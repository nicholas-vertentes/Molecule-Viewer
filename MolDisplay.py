import molecule;

# Predefined Constants
header = """<svg version="1.1" width="1000" height="1000"
 xmlns="http://www.w3.org/2000/svg">""";

footer = """</svg>""";

offsetx = 500;
offsety = 500;

# Atom Wrapper Class
class Atom:
    #Initilize Atom Class
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = c_atom.z

    #String representation of Atom class
    def __str__(self):
        return '''%s: %lf %lf %lf''' % (self.atom.element, self.atom.x, self.atom.y, self.atom.z)

    #SVG representation of Atom class
    def svg(self):
        cx = ((self.atom.x * 100.0) + offsetx)

        cy = ((self.atom.y * 100.0) + offsety)

        r = radius[self.atom.element]

        fill = element_name[self.atom.element]

        return '''  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n''' % (cx, cy, r, fill)

#Bond Wrapper Class
class Bond:
    #Initializing Bond Class
    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = c_bond.z

    #String representation of Bond class
    def __str__(self):
        return '''x1: %lf, x2: %lf, y1: %lf, y2: %lf, z: %lf, len: %lf, dx: %lf, dy: %lf, epairs: %d''' % (self.bond.x1, self.bond.x2, self.bond.y1, self.bond.y2, self.z, self.bond.len, self.bond.dx, self.bond.dy, self.bond.epairs)

    #SVG representation of Atom class
    def svg(self):
        #Calculate the coordinates of the corners of the rectangle that will reprsent the bond         
        cx1 = ((self.bond.x1 * 100.0) + offsetx)
        cy1 = ((self.bond.y1 * 100.0) + offsety)
        cx2 = ((self.bond.x2 * 100.0) + offsetx)
        cy2 = ((self.bond.y2 * 100.0) + offsety)

        point1x = (cx1 - (self.bond.dy * 10.0))
        point1y = (cy1 + (self.bond.dx * 10.0))

        point2x = (cx1 + (self.bond.dy * 10.0))
        point2y = (cy1 - (self.bond.dx * 10.0))

        point3x = (cx2 + (self.bond.dy * 10.0))
        point3y = (cy2 - (self.bond.dx * 10.0))

        point4x = (cx2 - (self.bond.dy * 10.0))
        point4y = (cy2 + (self.bond.dx * 10.0))


        return '''  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n''' % (point1x, point1y, point2x, point2y, point3x, point3y, point4x, point4y)

#"Molecule" class that inherits from the "molecule" class
class Molecule(molecule.molecule):
    #String representation of all bonds and atoms within the molecule
    def __str__(self):
        string = ""
        for i in range(self.atom_no):
            atom = Atom(self.get_atom(i))
            string += 'Atom %d: %s\n' % ((i + 1), atom.__str__())
        for i in range(self.bond_no):
            bond = Bond(self.get_bond(i))
            string += 'Bond %d: %s\n' % ((i + 1), bond.__str__())
        return string
    
    #svg representation of the molecule
    def svg(self):
        string = header
        i = 0
        j = 0
        while i < self.atom_no and j < self.bond_no:
            atom = Atom(self.get_atom(i))
            bond = Bond(self.get_bond(j))
            if atom.z < bond.z:
                string += atom.svg()
                i += 1
            else:
                string += bond.svg()
                j += 1

        while i < self.atom_no:
            atom = Atom(self.get_atom(i))
            string += atom.svg()
            i += 1

        while j < self.bond_no:
            bond = Bond(self.get_bond(j))
            string += bond.svg()
            j += 1

        string += footer

        return string

    #creates a molecule from a parsing a .sdf file
    def parse(self, file):

        for i in range(3):
            file.readline()

        splitStr = file.readline().split()
        numAtoms = int(splitStr[0])
        numBonds = int(splitStr[1])

        for i in range(numAtoms):
            splitStr = file.readline().split()
            self.append_atom(str(splitStr[3]), float(splitStr[0]), float(splitStr[1]), float(splitStr[2]))

        for i in range(numBonds):
            splitStr = file.readline().split()
            self.append_bond(int(splitStr[0]) - 1, int(splitStr[1]) - 1, int(splitStr[2]))

        return


        
#executed if this file is run as main program
#used for testing
if __name__ == "__main__":

    mol = Molecule()
    file = open('CID_31260.sdf', 'r')
    mol.parse(file)
    mol.sort()
    print(mol.svg())
