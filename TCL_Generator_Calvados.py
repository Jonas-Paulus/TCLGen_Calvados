import argparse

#parser IO
parser = argparse.ArgumentParser(
                    prog='TCL-Generator for Calvados',
                    description='Takes a calvados topology.pdb and generates a TCL sctipt to tell VMD which Atoms are bond.',
                    epilog='END')
parser.add_argument('filename') 
args = parser.parse_args()

#topology_file = "hnRNPA1LCD_1/top.pdb"
topology_file = args.filename

output_file = """set blist {}
"""
entry_string = lambda x: f"lappend blist [list {x-1} {x} A-A]\n"
atom_index = -1
last_resid = 1000 #some index >0
with open(topology_file) as inp:
    for line in inp:
        split = line.split()
        if split[0] == "ATOM":
            resid = int(split[5])
            atom_index += 1
            if resid == last_resid+1:
                #if this is a bond atom
                output_file += entry_string(atom_index)
            last_resid = resid
            


output_file += "topo setbondlist type $blist"
with open("topolog.tcl", "w") as w:
    w.write(output_file)