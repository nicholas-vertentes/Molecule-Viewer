#use port 58328

import sys;
from http.server import HTTPServer, BaseHTTPRequestHandler;
import molsql
import io
import urllib;

db = molsql.Database(reset=True);
db.create_tables();

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path == "/":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( 'index.html' ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/script.js":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/javascript" );

            fp = open( 'script.js' ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/style.css":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/css" );

            fp = open( 'style.css' ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );

    def do_POST(self):
        if self.path == "/":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            fp = open( 'index.html' ); 
            page = fp.read();
            fp.close();

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/addElement.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            page = """<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">

                        <title>Molecule Assignment</title>
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                        <script src="script.js"></script>
                        <link rel="stylesheet" type="text/css" href="style.css" />
                    </head>
                    <body>
                        <FORM method="POST" action="/">
                            <INPUT type="submit" value="Home" />
                        </FORM>

                        <h1>
                            Add Element
                        </h1>

                        <label>Element Number:</label>
                        <input type="text" id="enterElementNumber" />
                        <br/>
                        <br/>

                        <label>Element Code:</label>
                        <input type="text" id="enterElementCode" />
                        <br/>
                        <br/>

                        <label>Element Name:</label>
                        <input type="text" id="enterElementName" />
                        <br />
                        <br />

                        <label>Hex Colour 1:</label>
                        <input type="text" id="enterColour1" />
                        <br />
                        <br />

                        <label>Hex Colour 2:</label>
                        <input type="text" id="enterColour2" />
                        <br />
                        <br />

                        <label>Hex Colour 3:</label>
                        <input type="text" id="enterColour3" />
                        <br />
                        <br />

                        <label>Element Radius:</label>
                        <input type="text" id="enterElementRadius" />
                        <br />
                        <br />

                        <FORM method="POST" action="addElement.html">
                            <INPUT type="submit" value="Clear" />
                        </FORM>
                        <br/>

                        <button id="addElementButton"> Submit </button>
                        

                    </body>
                    </html>"""

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/addElement_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            addedElement = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            try:
                db['Elements'] = '''( %d, '%s', '%s', '%s', '%s', '%s', %d )''' % (int(addedElement['Element_Number'][0]), str(addedElement['Element_Code'][0]), str(addedElement['Element_Name'][0]), str(addedElement['Colour1'][0]), str(addedElement['Colour2'][0]), str(addedElement['Colour3'][0]), int(addedElement['Element_Radius'][0]))

                message = "Element Added";
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );
                
            except molsql.sqlite3.IntegrityError:
                message = "Element already exists in table"
                self.send_response( 200 );
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );
               
        elif self.path == "/removeElement.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            page = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">

                            <title>Molecule Assignment</title>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                            <script src="script.js"></script>
                            <link rel="stylesheet" type="text/css" href="style.css" />
                        </head>
                        <body>
                            <FORM method="POST" action="/">
                                <INPUT type="submit" value="Home" />
                            </FORM>

                            <h1>
                                Remove Element
                            </h1>

                            <label>Element Code:</label>
                            <input type="text" id="removeElementCode" />
                            <button id="removeElementButton"> Submit </button>
                            <br/>
                            <br/>

                            <FORM method="POST" action="removeElement.html">
                                <INPUT type="submit" value="Refresh" />
                            </FORM>"""

            element_dictionary = db.element_name()
            for element in element_dictionary:
                page += '''<p class = element_list>'''
                page += str(element) + ': ' + str(element_dictionary[element])
                page += '''</p>'''

            page += """
                        </body>
                        </html>"""

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/removeElement_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            removedElement = urllib.parse.parse_qs( body.decode( 'utf-8' ) );

            element_dictionary = db.element_name()
            elementList = list(element_dictionary.keys())

            if (str(removedElement['Element_Code'][0])) not in elementList:
                message = "Element does not exist in database";
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );

            else:
                db.connection.execute(
                    """DELETE FROM Elements 
                    WHERE ELEMENT_CODE = '%s';""" % (str(removedElement['Element_Code'][0]))
                )
                message = "Element Removed";
                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/plain" );
                self.send_header( "Content-length", len(message) );
                self.end_headers();
                self.wfile.write( bytes( message, "utf-8" ) );
            
        elif self.path == "/uploadSDF.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            page = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">

                            <title>Molecule Assignment</title>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                            <script src="script.js"></script>
                            <link rel="stylesheet" type="text/css" href="style.css" />
                        </head>
                        <body>
                            <FORM method="POST" action="/">
                                <INPUT type="submit" value="Home" />
                            </FORM>

                            <h1> Upload SDF File </h1>

                             <form action="uploadSDF_handler.html" enctype="multipart/form-data" method="post">
                                <p>
                                    <label> Molecule Name </label>
                                    <input type="text" id="moleculeName" name="moleculeNameTextfield"/>
                                </p>
                                <p>
                                    <input type="file" id="sdf_file" name="filename"/>
                                </p>  
                                <p>
                                    <input type="submit" value="Upload""/>
                                </p>
                            </form>
                        </body>
                        </html>"""

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/uploadSDF_handler.html":

            text_io = io.TextIOWrapper(self.rfile)

            for i in range(3):
                text_io.readline()

            moleculeName = text_io.readline()[:-1]

            for i in range(4):
                text_io.readline()
            
            try:
                if moleculeName != "":
                    db.add_molecule(moleculeName, text_io)

                    page = """<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                    <title>Molecule Assignment</title>
                                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                    <script src="script.js"></script>
                                    <link rel="stylesheet" type="text/css" href="style.css" />
                                </head>
                                <body>
                                    <h1> Molecule Uploaded Successfully! </h1>
                                    <FORM method="POST" action="uploadSDF.html">
                                        <INPUT type="submit" value="Continue" />
                                    </FORM>
                                </body>
                                </html>"""

                else:
                    page = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                <title>Molecule Assignment</title>
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                <script src="script.js"></script>
                                <link rel="stylesheet" type="text/css" href="style.css" />
                            </head>
                            <body>
                                <h1> Please Enter Molecule Name! </h1>
                                <FORM method="POST" action="uploadSDF.html">
                                    <INPUT type="submit" value="Continue" />
                                </FORM>
                            </body>
                            </html>"""

            except molsql.sqlite3.IntegrityError:

                page = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                <title>Molecule Assignment</title>
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                <script src="script.js"></script>
                                <link rel="stylesheet" type="text/css" href="style.css" />
                            </head>
                            <body>
                                <h1> Molecule Already Exists in Database! </h1>
                                <FORM method="POST" action="uploadSDF.html">
                                    <INPUT type="submit" value="Continue" />
                                </FORM>
                            </body>
                            </html>"""

            except Exception:

                page = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                <title>Molecule Assignment</title>
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                <script src="script.js"></script>
                                <link rel="stylesheet" type="text/css" href="style.css" />
                            </head>
                            <body>
                                <h1> Invalid File! </h1>
                                <FORM method="POST" action="uploadSDF.html">
                                    <INPUT type="submit" value="Continue" />
                                </FORM>
                            </body>
                            </html>"""

            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/selectMolecule.html":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );

            page = """<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">

                            <title>Molecule Assignment</title>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                            <script src="script.js"></script>
                            <link rel="stylesheet" type="text/css" href="style.css" />
                        </head>
                        <body>
                            <FORM method="POST" action="/">
                                <INPUT type="submit" value="Home" />
                            </FORM>

                            <h1> Select Molecule </h1>"""

            moleculeTable = db.connection.execute(
                """ SELECT NAME FROM Molecules"""
            )

            for molecule in moleculeTable:
                mol = db.load_mol(molecule[0])
                page += '''<p class=element_list>'''
                page += '''%s: %d Atoms, %d Bonds''' % (str(molecule[0]), mol.atom_no, mol.bond_no)
                page += '''</p>'''


            page += """ <form action="molecule" enctype="multipart/form-data" method="post">
                            <p>
                                <label> Molecule Name </label>
                                <input type="text" id="moleculeSelection" name="moleculeSelectionTextfield"/>
                            </p>
                            <p>
                                <input type="submit" value="Display""/>
                            </p>
                        </form>
                        </body>
                        </html>"""

            self.send_header( "Content-length", len(page) );
            self.end_headers();
            self.wfile.write( bytes( page, "utf-8" ) );

        elif self.path == "/molecule":

            text_io = io.TextIOWrapper(self.rfile)

            for i in range(3):
                text_io.readline()

            moleculeName = text_io.readline()[:-1]

            if moleculeName != "":

                moleculeTable = db.connection.execute(
                """ SELECT NAME FROM Molecules"""
                )
                moleculeList = []

                for molecule in moleculeTable:
                    moleculeList.append(molecule[0])

                if moleculeName in moleculeList:

                    moleculeElements = db.connection.execute(
                    """ SELECT DISTINCT ELEMENT_CODE FROM Atoms INNER JOIN (SELECT ATOM_ID AS MoleculeAtomJoin FROM MoleculeAtom WHERE (MoleculeAtom.MOLECULE_ID = (Select MOLECULE_ID FROM Molecules WHERE NAME = '%s'))) ON (Atoms.ATOM_ID = MoleculeAtomJoin);""" % (moleculeName)
                    )

                    element_dictionary = db.element_name()
                    elementList = list(element_dictionary.keys())

                    i=0
                    for element in moleculeElements:
                        if str(element[0]) not in elementList:
                            i = i + 1
                            db['Elements'] = '''( 0, '%s', 'temp%s', '000000', '000000', '000000', 40 )''' % (str(element[0]), str(i))


                    molsql.MolDisplay.radius = db.radius();
                    molsql.MolDisplay.element_name = db.element_name();
                    molsql.MolDisplay.header += db.radial_gradients();

                    mol = db.load_mol(moleculeName)
                    mol.sort()

                    page = """<!DOCTYPE html>
                                <html lang="en">
                                <head>
                                    <meta charset="UTF-8">
                                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                    <title>Molecule Assignment</title>
                                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                    <script src="script.js"></script>
                                    <link rel="stylesheet" type="text/css" href="style.css" />
                                </head>
                                <body>

                                    <FORM method="POST" action="selectMolecule.html">
                                        <INPUT type="submit" value="Back" />
                                    </FORM>

                                    <h1 id="rotationMoleculeName">
                                        %s
                                    </h1>

                                    <h3>
                                        Degree Rotation
                                    </h3>

                                    <label> X-Rotation </label>
                                    <input type="text" id="x-rotationText" value="0"/>
                                    <br/>
                                    <br/>

                                    <label> Y-Rotation </label>
                                    <input type="text" id="y-rotationText" value="0"/>
                                    <br/>
                                    <br/>

                                    <label> Z-Rotation </label>
                                    <input type="text" id="z-rotationText" value="0"/>
                                    <br/>
                                    <br/>

                                    <button id="xyz-rotationButton"> Rotate </button>    
                                    <br/>
                                    <br/>
                                    <button id="resetRotationButton"> Reset </button>
                                    <br/>
                                    
                                    <div id="svg_box">
                                        %s
                                    </div>
                                    
                                </body>
                                </html>""" % (moleculeName, mol.svg())

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header("Content-length", len(page))
                    self.end_headers()
                    self.wfile.write( bytes( page, "utf-8" ) )

                    db.connection.execute(
                        """DELETE FROM Elements 
                        WHERE ELEMENT_NAME LIKE 'temp%';"""
                    )

                else:
                    page = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                <title>Molecule Assignment</title>
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                <script src="script.js"></script>
                                <link rel="stylesheet" type="text/css" href="style.css" />
                            </head>
                            <body>
                                <h1> Molecule not in Database! </h1>
                                <FORM method="POST" action="selectMolecule.html">
                                    <INPUT type="submit" value="Continue" />
                                </FORM>
                            </body>
                            </html>"""

                    self.send_response( 200 ); # OK
                    self.send_header( "Content-type", "text/html" );
                    self.send_header( "Content-length", len(page) );
                    self.end_headers();
                    self.wfile.write( bytes( page, "utf-8" ) );


            else:
                page = """<!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                <meta name="viewport" content="width=device-width, initial-scale=1.0">

                                <title>Molecule Assignment</title>
                                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"> </script>
                                <script src="script.js"></script>
                                <link rel="stylesheet" type="text/css" href="style.css" />
                            </head>
                            <body>
                                <h1> Please Enter Molecule Name! </h1>
                                <FORM method="POST" action="selectMolecule.html">
                                    <INPUT type="submit" value="Continue" />
                                </FORM>
                            </body>
                            </html>"""

                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "text/html" );
                self.send_header( "Content-length", len(page) );
                self.end_headers();
                self.wfile.write( bytes( page, "utf-8" ) );
                

        elif self.path == "/xyz-rotation_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            moleculeAndRotation = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            xrotationDegree = moleculeAndRotation['X_Rotation'][0]
            yrotationDegree = moleculeAndRotation['Y_Rotation'][0]
            zrotationDegree = moleculeAndRotation['Z_Rotation'][0]
            moleculeName = moleculeAndRotation['Molecule_Name'][0].strip()
            # print(xrotationDegree + yrotationDegree + zrotationDegree + moleculeName)

            moleculeElements = db.connection.execute(
            """ SELECT DISTINCT ELEMENT_CODE FROM Atoms INNER JOIN (SELECT ATOM_ID AS MoleculeAtomJoin FROM MoleculeAtom WHERE (MoleculeAtom.MOLECULE_ID = (Select MOLECULE_ID FROM Molecules WHERE NAME = '%s'))) ON (Atoms.ATOM_ID = MoleculeAtomJoin);""" % (moleculeName)
            )

            element_dictionary = db.element_name()
            elementList = list(element_dictionary.keys())

            i=0
            for element in moleculeElements:
                if str(element[0]) not in elementList:
                    i = i + 1
                    db['Elements'] = '''( 0, '%s', 'temp%s', '000000', '000000', '000000', 40 )''' % (str(element[0]), str(i))


            molsql.MolDisplay.radius = db.radius();
            molsql.MolDisplay.element_name = db.element_name();
            molsql.MolDisplay.header += db.radial_gradients();

            mol = db.load_mol(moleculeName)

            mx = molsql.MolDisplay.molecule.mx_wrapper(int(xrotationDegree),0,0)
            mol.xform(mx.xform_matrix)

            mx = molsql.MolDisplay.molecule.mx_wrapper(0,int(yrotationDegree),0)
            mol.xform(mx.xform_matrix)

            mx = molsql.MolDisplay.molecule.mx_wrapper(0,0,int(zrotationDegree))
            mol.xform(mx.xform_matrix)

            mol.sort()
            message = mol.svg()

            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );

            db.connection.execute(
                """DELETE FROM Elements 
                WHERE ELEMENT_NAME LIKE 'temp%';"""
            )


        elif self.path == "/resetRotation_handler.html":
            content_length = int(self.headers['Content-Length']);
            body = self.rfile.read(content_length);

            resetMolecule = urllib.parse.parse_qs( body.decode( 'utf-8' ) );
            moleculeName = resetMolecule['Molecule_Name'][0].strip()

            moleculeElements = db.connection.execute(
            """ SELECT DISTINCT ELEMENT_CODE FROM Atoms INNER JOIN (SELECT ATOM_ID AS MoleculeAtomJoin FROM MoleculeAtom WHERE (MoleculeAtom.MOLECULE_ID = (Select MOLECULE_ID FROM Molecules WHERE NAME = '%s'))) ON (Atoms.ATOM_ID = MoleculeAtomJoin);""" % (moleculeName)
            )

            element_dictionary = db.element_name()
            elementList = list(element_dictionary.keys())

            i=0
            for element in moleculeElements:
                if str(element[0]) not in elementList:
                    i = i + 1
                    db['Elements'] = '''( 0, '%s', 'temp%s', '000000', '000000', '000000', 40 )''' % (str(element[0]), str(i))


            molsql.MolDisplay.radius = db.radius();
            molsql.MolDisplay.element_name = db.element_name();
            molsql.MolDisplay.header += db.radial_gradients();

            mol = db.load_mol(moleculeName)
            mol.sort()
            message = mol.svg()

            self.send_response( 200 );
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(message) );
            self.end_headers();
            self.wfile.write( bytes( message, "utf-8" ) );

            db.connection.execute(
                """DELETE FROM Elements 
                WHERE ELEMENT_NAME LIKE 'temp%';"""
            )

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );


#creates server on command line specified port and serves it
httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever(); 
