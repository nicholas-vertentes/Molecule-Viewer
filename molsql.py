import sqlite3
import os
import MolDisplay

class Database:
    # Initialize Database class
    def __init__ (self, reset=False):
        # Delete .db if reset is set to TRUE
        if reset == True:
            if os.path.exists( 'molecules.db' ):
                os.remove( 'molecules.db' )
        self.connection = sqlite3.connect('molecules.db')

    # Create Database tables
    def create_tables(self):
        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS Elements
                (ELEMENT_NO     INTEGER NOT NULL,
                ELEMENT_CODE    VARCHAR(3) PRIMARY KEY NOT NULL,
                ELEMENT_NAME    VARCHAR(32) NOT NULL,
                COLOUR1         CHAR(6) NOT NULL,
                COLOUR2         CHAR(6) NOT NULL,
                COLOUR3         CHAR(6) NOT NULL,
                RADIUS          DECIMAL(3) NOT NULL);""")

        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS Atoms
                (ATOM_ID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE    VARCHAR(3) NOT NULL,
                X               DECIMAL(7,4) NOT NULL,
                Y               DECIMAL(7,4) NOT NULL,
                Z               DECIMAL(7,4) NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""")

        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS Bonds
                (BOND_ID        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1              INTEGER NOT NULL,
                A2              INTEGER NOT NULL,
                EPAIRS          INTEGER NOT NULL);""")

        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS Molecules
                (MOLECULE_ID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME            TEXT UNIQUE NOT NULL);""")

        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS MoleculeAtom
                (MOLECULE_ID    INTEGER NOT NULL,
                ATOM_ID         INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (ATOM_ID) REFERENCES Atoms);""")

        self.connection.execute(
            """ CREATE TABLE IF NOT EXISTS MoleculeBond
                (MOLECULE_ID    INTEGER NOT NULL,
                BOND_ID         INTEGER NOT NULL,
                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (BOND_ID) REFERENCES Bonds);""")

    # Provides fuctionality to index into a table and add records
    def __setitem__(self, table, values):
        self.connection.execute(
            """ INSERT INTO %s
                VALUES %s;""" % (table, str(values))
            )

    # Adds an atom to the Atoms table
    # Links the added atom to the specified molecule in the MoleculeAtom table
    def add_atom(self, molname, atom):
        atomAttributes = """('%s', %lf, %lf, %lf)""" % (atom.atom.element, atom.atom.x, atom.atom.y, atom.atom.z)

        self.connection.execute(
            """ INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z)
            VALUES %s;""" % atomAttributes
        )

        # Gets the ATOM_ID of most recently inserted atom
        atomID = self.connection.execute(
            """ SELECT MAX(ATOM_ID) FROM Atoms;"""
        )

        # Gets the MOLECULE_ID of the specified Molecule
        moleculeID = self.connection.execute(
            """ SELECT MAX(MOLECULE_ID) FROM Molecules WHERE NAME = '%s';""" % (molname)
        )

        # Create a string representation of a tuple using ATOM_ID and MOLECULE_ID
        MoleculeAtomAttributes = '('
        for row in moleculeID:
            MoleculeAtomAttributes += str(row[0])
        MoleculeAtomAttributes += ', '
        for row in atomID:
            MoleculeAtomAttributes += str(row[0])
        MoleculeAtomAttributes += ')'

        # Link the ATOM_ID to the MOLECULE_ID in the MoleculeAtom table
        self.connection.execute(
            """ INSERT 
                INTO MoleculeAtom(MOLECULE_ID, ATOM_ID)
                VALUES %s;""" % MoleculeAtomAttributes
        )

    # Serves the same function as add_atom, but with bonds instead
    def add_bond(self, molname, bond):
        bondAttributes = """(%d, %d, %d)""" % (bond.bond.a1, bond.bond.a2, bond.bond.epairs)

        self.connection.execute(
            """ INSERT INTO Bonds(A1, A2, EPAIRS)
            VALUES %s;""" % bondAttributes
        )

        bondID = self.connection.execute(
            """ SELECT MAX(BOND_ID) FROM Bonds;""" 
        )

        moleculeID = self.connection.execute(
            """ SELECT MAX(MOLECULE_ID) FROM Molecules WHERE NAME = '%s';""" % (molname)
        )

        MoleculeBondAttributes = '('
        for row in moleculeID:
            MoleculeBondAttributes += str(row[0])
        MoleculeBondAttributes += ', '
        for row in bondID:
            MoleculeBondAttributes += str(row[0])
        MoleculeBondAttributes += ')'

        self.connection.execute(
            """ INSERT 
                INTO MoleculeBond(MOLECULE_ID, BOND_ID)
                VALUES %s;""" % (MoleculeBondAttributes)
        )
    
    # Adds the attributes of the molecule represented in an .SDF file to the corresponding database tables
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol.parse(fp)

        # Add the molecule name to the Molecules table
        self.connection.execute(
            """ INSERT 
                INTO Molecules(NAME)
                VALUES ('%s');""" % (name)
        )

        # Add all atoms and bonds in the molecule to the Atoms and Bonds tables, respectively
        for i in range(mol.atom_no):
            atom = MolDisplay.Atom(mol.get_atom(i))
            self.add_atom(name, atom)
        for i in range(mol.bond_no):
            bond = MolDisplay.Bond(mol.get_bond(i))
            self.add_bond(name, bond)

    # Gets the attributes of the specified molecule from the corresponding database tables
    # Uses the collected attributes to initialize and return a Molecule object
    def load_mol(self, name):
        # Initialize a Molecule object
        mol = MolDisplay.Molecule()

        # Get a table of the atoms that are associated with the specified molecule
        organizedAtoms = self.connection.execute(
            """ SELECT ELEMENT_CODE, X, Y, Z FROM Atoms INNER JOIN (SELECT ATOM_ID AS MoleculeAtomJoin FROM MoleculeAtom WHERE (MoleculeAtom.MOLECULE_ID = (Select MOLECULE_ID FROM Molecules WHERE NAME = '%s'))) ON (Atoms.ATOM_ID = MoleculeAtomJoin) ORDER BY ATOM_ID ASC;""" % (name)
        )

        # Add each atom from the above table to the Molecule object
        for atom in organizedAtoms:
            mol.append_atom(str(atom[0]), float(atom[1]), float(atom[2]), float(atom[3]))

        # Get a table of the bonds that are associated with the specified molecule
        organizedBonds = self.connection.execute(
            """ SELECT A1, A2, EPAIRS FROM Bonds INNER JOIN (SELECT BOND_ID AS MoleculeBondJoin FROM MoleculeBond WHERE (MoleculeBond.MOLECULE_ID = (Select MOLECULE_ID FROM Molecules WHERE NAME = '%s'))) ON (Bonds.BOND_ID = MoleculeBondJoin) ORDER BY BOND_ID ASC;""" % (name)
        )

        # Add each bond from the above table to the Molecule object
        for bond in organizedBonds:
            mol.append_bond(int(bond[0]), int(bond[1]), int(bond[2]))

        # Return the Molecule object
        return mol

    # Create and return a dictionary with: (key = ELEMENT_CODE, value = RADIUS) from the Elements tables
    def radius(self):
        radius_dict = {}
        
        radiusElementTable = self.connection.execute(
            """ SELECT ELEMENT_CODE, RADIUS FROM Elements;"""
        )

        for radiusElement in radiusElementTable:
            radius_dict[str(radiusElement[0])] = int(radiusElement[1])

        return radius_dict

    # Create and return a dictionary with: (key = ELEMENT_CODE, value = ELEMENT_NAME) from the Elements tables
    def element_name(self):
        elementName_dict = {}
        
        elementNameTable = self.connection.execute(
            """ SELECT ELEMENT_CODE, ELEMENT_NAME FROM Elements;"""
        )

        for elementName in elementNameTable:
            elementName_dict[str(elementName[0])] = str(elementName[1])

        return elementName_dict

    # Returns a set of concatenated strings that provide SVG functionality
    # Maps each element to its corresponding colour set from the Elements table
    def radial_gradients(self):
        radialGradientSVG = ""

        elementTable = self.connection.execute(
            """SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM Elements;"""
        )

        for element in elementTable:
            radialGradientSVG += """
    <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/>
        <stop offset="50%%" stop-color="#%s"/>
        <stop offset="100%%" stop-color="#%s"/>
    </radialGradient>""" % (str(element[0]), str(element[1]), str(element[2]), str(element[3]))

        return radialGradientSVG

# if __name__ == "__main__":
#     db = Database(reset=True);
#     db.create_tables();

#     db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
#     db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
#     db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
#     db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );

#     fp = open( 'water-3D-structure-CT1000292221.sdf' );
#     db.add_molecule( 'Water', fp );
#     fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
#     db.add_molecule( 'Caffeine', fp );
#     fp = open( 'CID_31260.sdf' );
#     db.add_molecule( 'Isopentanol', fp );

    # display tables
    # print( db.connection.execute( "SELECT * FROM Elements;" ).fetchall() );
    # print()
    # print( db.connection.execute( "SELECT * FROM Molecules;" ).fetchall() );
    # print()
    # print( db.connection.execute( "SELECT * FROM Atoms;" ).fetchall() );
    # print()
    # print( db.connection.execute( "SELECT * FROM Bonds;" ).fetchall() );
    # print()
    # print( db.connection.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    # print()
    # print( db.connection.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );

    # print(db.connection.execute( "SELECT name FROM sqlite_master WHERE type='table';" ).fetchall())



#     MolDisplay.radius = db.radius();
#     MolDisplay.element_name = db.element_name();
#     MolDisplay.header += db.radial_gradients();

#     for molecule in [ 'Water', 'Caffeine', 'Isopentanol' ]:
#        mol = db.load_mol( molecule );
#        mol.sort();
#        fp = open( molecule + ".svg", "w" );
#        fp.write( mol.svg() );
#        fp.close();