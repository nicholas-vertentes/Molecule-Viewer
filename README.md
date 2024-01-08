# Molecule-Viewer
Software Systems Development &amp; Integration (CIS*2750) Project

To Execute:\
1 - Use a Linux/Unix enviornment\
2 - Navigate to the folder using CLI\
3 - Execute the command: <code>make</code>\
4 - Execute the command: <code>export LD_LIBRARY_PATH=\`pwd\`</code>\
5 - Execute the command: <code>python3 server.py 1234</code>\
6 - Navigate to `localhost:1234` in a web browser\
7 - Execute the command  `ctrl + c` to stop server

Notes:\
~ The <a href="./makefile">makefile</a> may need to be updated to access the <Python.h> library\
~ The <a href="./Test Files">Test Files</a> can be executed with the command `clang -L. -Wall -std=c99 -pedantic -lm test1.c -lmol -o a.out`
