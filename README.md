This is a simple python script to generate a TCL script which can be loaded in VMD to visualise the bonds in a calvados simulation.
It can be executed via 
python TCL_Generator_Calvados.py [patht/topology.pdb]
The TCL script will be saved in the folder of the script. 

Planned changes:
- use the xml file instead pdb to get valid bond info
- include an -o flag to allow to specify a location for the output.
