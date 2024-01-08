#include "mol.h"

void atomset(atom *atom, char element[3], double *x, double *y, double *z){
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z){
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;

    compute_coords(bond);
}

void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs){
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

void compute_coords(bond *bond){
    double x1;
    double x2;
    double y1;
    double y2;
    double z;
    double len;
    double dx;
    double dy;

    /*Calculate attributes*/
    x1 = bond->atoms[bond->a1].x;
    y1 = bond->atoms[bond->a1].y;

    x2 = bond->atoms[bond->a2].x;
    y2 = bond->atoms[bond->a2].y;

    z = ((bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2);

    len = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2));

    dx = (x2 - x1) / len;
    dy = (y2 - y1) / len;

    /*Store attributes in bond*/
    bond->x1 = x1;
    bond->x2 = x2;
    bond->y1 = y1;
    bond->y2 = y2;
    bond->z = z;
    bond->len = len;
    bond->dx = dx;
    bond->dy = dy;
}

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max){

    molecule *temp = (molecule*)malloc(sizeof(molecule));
    if (temp == NULL)
    {
        fprintf(stderr, "Memory Allocation Failed\n");  //standard memory allocation error checking code used throughout program
        exit(1);
    }

    temp->atom_max = atom_max;
    temp->atom_no = 0;

    temp->atoms = (atom *)malloc(atom_max * sizeof(atom));
    if (temp->atoms == NULL)
    {
        fprintf(stderr, "Memory Allocation Failed\n");
        exit(1);
    }

    for (int i = 0; i < atom_max; i++){
        strcpy(temp->atoms[i].element, "\0");   //initializes each atom within the molecule to empty
        temp->atoms[i].x = 0.0;
        temp->atoms[i].y = 0.0;
        temp->atoms[i].z = 0.0;
    }

    temp->atom_ptrs = (atom **)malloc(atom_max * sizeof(atom *));
    if (temp->atom_ptrs == NULL)
    {
        fprintf(stderr, "Memory Allocation Failed\n");
        exit(1);
    }

    for (int i = 0; i < atom_max; i++)
    {
        temp->atom_ptrs[i] = NULL;  //initializes each atom pointer within the molecule to empty
    }

    temp->bond_max = bond_max;
    temp->bond_no = 0;

    temp->bonds = (bond *)malloc(bond_max * sizeof(bond));
    if (temp->bonds == NULL)
    {
        fprintf(stderr, "Memory Allocation Failed\n");
        exit(1);
    }

    for (int i = 0; i < bond_max; i++)  //initializes each bond within the molecule to empty
    {
        temp->bonds[i].atoms = NULL;
    }

    temp->bond_ptrs = (bond **)malloc(bond_max * sizeof(bond *));
    if (temp->bond_ptrs == NULL)
    {
        fprintf(stderr, "Memory Allocation Failed\n");
        exit(1);
    }

    for (int i = 0; i < bond_max; i++)  //initializes each bond pointer within the molecule to empty
    {
        temp->bond_ptrs[i] = NULL;
    }

    return temp;
}

molecule *molcopy(molecule *src){

    molecule *temp;

    temp = molmalloc(src->atom_max, src->bond_max);

    for (int i = 0; i < src->atom_no; i++)
    {
        molappend_atom(temp, &(src->atoms[i]));     //appends each atom from src molecule to new molecule
    }

    for (int i = 0; i < src->bond_no; i++)
    {
        molappend_bond(temp, &(src->bonds[i]));       //appends each bond from src molecule to new molecule
    }

    return temp;
}

void molfree(molecule *ptr){
    free(ptr->atoms);

    free(ptr->atom_ptrs);

    free(ptr->bonds);

    free(ptr->bond_ptrs);

    free(ptr);
}

void molappend_atom(molecule *molecule, atom *atom){

    if (molecule->atom_no == molecule->atom_max){   //increase atom_max to store more atoms and subsequently increase memory allocation
        if (molecule->atom_max == 0){
            molecule->atom_max += 1;
        }
        else{
            molecule->atom_max *= 2;
        }

        molecule->atoms = realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));
        if (molecule->atoms == NULL)
        {
            fprintf(stderr, "Memory Allocation Failed\n");
            exit(1);
        }
        for (int i = molecule->atom_no; i < molecule->atom_max; i++){   //initializes new atoms to empty
            strcpy(molecule->atoms[i].element, "\0");
            molecule->atoms[i].x = 0.0;
            molecule->atoms[i].y = 0.0;
            molecule->atoms[i].z = 0.0;
        }

        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));
        if (molecule->atom_ptrs == NULL)
        {
            fprintf(stderr, "Memory Allocation Failed\n");
            exit(1);
        }

        for (int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &(molecule->atoms[i]);     //atom pointers point to new atom array
        }

        for (int i = molecule->atom_no; i < molecule->atom_max; i++)    //initializes new atom pointers to empty
        {
            molecule->atom_ptrs[i] = NULL;
        }
    }
    
    for (int i = 0; i < molecule->atom_max; i++){
        if (strcmp(molecule->atoms[i].element, "\0") == 0   //looks for first empty atom within molecule
        && molecule->atoms[i].x == 0
        && molecule->atoms[i].y == 0
        && molecule->atoms[i].z == 0){
            strcpy(molecule->atoms[i].element, atom->element);
            molecule->atoms[i].x = atom->x;
            molecule->atoms[i].y = atom->y;
            molecule->atoms[i].z = atom->z;

            for (int j = 0; j < molecule->atom_max; j++){   //looks for first empty atom pointer within molecule
                if (molecule->atom_ptrs[j] == NULL){
                    molecule->atom_ptrs[j] = &(molecule->atoms[i]);
                    break;
                }
            }

            molecule->atom_no += 1;

            break;
        }
    }
}

void molappend_bond(molecule *molecule, bond *bond){
    
    if (molecule->bond_no == molecule->bond_max){   //increase bond_max to store more bonds and subsequently increase memory allocation
        if (molecule->bond_max == 0){
            molecule->bond_max += 1;
        }
        else{
            molecule->bond_max *= 2;
        }

        molecule->bonds = realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));
        if (molecule->bonds == NULL)
        {
            fprintf(stderr, "Memory Allocation Failed\n");
            exit(1);
        }

        for (int i = molecule->bond_no; i < molecule->bond_max; i++){   //initializes new bonds to empty
            molecule->bonds[i].atoms = NULL;
        }

        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));
        if (molecule->bond_ptrs == NULL)
        {
            fprintf(stderr, "Memory Allocation Failed\n");
            exit(1);
        }

        for (int i = 0; i < molecule->bond_no; i++)
        {
            molecule->bond_ptrs[i] = &(molecule->bonds[i]);     //bond pointers point to new bond array
        }

        for (int i = molecule->bond_no; i < molecule->bond_max; i++){   //initializes new bond pointers to empty
            molecule->bond_ptrs[i] = NULL;
        }
    }

    for (int i = 0; i < molecule->bond_max; i++){   //looks for the first empty bond within molecule
        if (molecule->bonds[i].atoms == NULL){
            molecule->bonds[i] = *bond;

            for (int j = 0; j < molecule->bond_max; j++){   //looks for the first empty bond pointer within molecule
                if (molecule->bond_ptrs[j] == NULL){
                    molecule->bond_ptrs[j] = &(molecule->bonds[i]);
                    break;
                }
            }

            molecule->bond_no += 1;

            break;
        }
    }
}

void molsort(molecule *molecule){

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), compareAtoms);    //uses helper functions to ordering elements

    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), bond_comp);
}

int compareAtoms(const void* x, const void* y){     //sort atoms by increasing z value

    atom *atom1 = *(atom **)x;
    atom *atom2 = *(atom **)y;

    double result = (atom1->z - atom2->z);  //variable "result" is not returned as it would be truncated to an int (leading to improper ordering)

    if (result > 0.0){
        return 1;   //x should go after y
    }
    else if(result < 0.0){
        return -1;  //x should go before y
    }
    
    return 0;   //x is equivalent to y
}

int bond_comp(const void* a, const void* b){     //sort bonds by increasing "z value"

    bond *bond1 = *(bond **)a;
    bond *bond2 = *(bond **)b;

    double bond1Avg = bond1->z;     //z value is the avaerage z value of the 
    double bond2Avg = bond2->z;     //two atoms in the bond

    double result = (bond1Avg - bond2Avg);  //variable "result" is not returned as it would be truncated to an int (leading to improper ordering)

    if (result > 0.0)
    {
        return 1;   //x should go after y
    }
    else if (result < 0.0)
    {
        return -1;  //x should go before y
    }

    return 0;   //x is equivalent to y
}

void xrotation(xform_matrix xform_matrix, unsigned short deg){

    double rad = deg * (M_PI / 180.0);

    xform_matrix[0][0] = 1;     //x-transformation matrix
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

void yrotation(xform_matrix xform_matrix, unsigned short deg){

    double rad = deg * (M_PI / 180.0);

    xform_matrix[0][0] = cos(rad);  //y-transformation matrix
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

void zrotation(xform_matrix xform_matrix, unsigned short deg){

    double rad = deg * (M_PI / 180.0);

    xform_matrix[0][0] = cos(rad);  //z-transformation matrix
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

void mol_xform(molecule *molecule, xform_matrix matrix){

    for (int i = 0; i < molecule->atom_no; i++){
        double original[3] = {
            molecule->atoms[i].x,
            molecule->atoms[i].y,
            molecule->atoms[i].z,   //array of original coordinates of atom
        };
        double result[3] = {0, 0, 0};

        //final coordinates of atom are computed using matrix multiplication and stored in array "result"
        for (int rows = 0; rows < 3; rows++){
            for (int columns = 0; columns < 3; columns++){
                result[rows] += (matrix[rows][columns] * original[columns]);
            }
        }

        molecule->atoms[i].x = result[0];   //the new coordinates are copied back into the atom
        molecule->atoms[i].y = result[1];
        molecule->atoms[i].z = result[2];
    }

    for (int i = 0; i < molecule->bond_no; i++){
        compute_coords(&(molecule->bonds[i]));      //update bond attributes
    }
}
