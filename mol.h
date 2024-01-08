#ifndef _mol_h
#define _mol_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

//execute if macro is not defined in math library
#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif


typedef struct atom
{
    char element[3];
    double x, y, z;
} atom;

typedef struct bond
{
    unsigned short a1, a2;
    unsigned char epairs;
    atom *atoms;
    double x1, x2, y1, y2, z, len, dx, dy;
} bond;

typedef struct molecule
{
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

typedef double xform_matrix[3][3];

typedef struct mx_wrapper
{
  xform_matrix xform_matrix;
} mx_wrapper;

void atomset(atom *atom, char element[3], double *x, double *y, double *z);

void atomget(atom *atom, char element[3], double *x, double *y, double *z);

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs);

void compute_coords(bond *bond);

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);

molecule *molcopy(molecule *src);

void molfree(molecule *ptr);

void molappend_atom(molecule *molecule, atom *atom);

void molappend_bond(molecule *molecule, bond *bond);

void molsort(molecule *molecule);

int compareAtoms(const void *x, const void *y);

int bond_comp(const void *a, const void *b);

void xrotation(xform_matrix xform_matrix, unsigned short deg);

void yrotation(xform_matrix xform_matrix, unsigned short deg);

void zrotation(xform_matrix xform_matrix, unsigned short deg);

void mol_xform(molecule *molecule, xform_matrix matrix);

// typedef struct rotations
// {
//   molecule *x[72];
//   molecule *y[72];
//   molecule *z[72];
// } rotations;

// rotations *spin( molecule *mol );
// void rotationsfree( rotations *rotations );

#endif
