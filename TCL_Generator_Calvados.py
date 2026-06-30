import argparse
import xml.etree.ElementTree as ET
import warnings
import re
import numpy as np


def bonds_from_xml(filename):
    #Generates bond atom pair iterator from xml file
    tree = ET.parse(filename)
    root = tree.getroot()
    forces = root.find("Forces")
    for force in forces:
        is_harmonic = False
        if force.attrib["name"] == "HarmonicBondForce":
            is_harmonic = True
        elif force.attrib["energy"] == "k*(r-r0)^2":
            is_harmonic = True

        if is_harmonic:
            bonds = force.find("Bonds")
            print(bonds[0].attrib)
            for bond in bonds:
                #print(bond.attrib)
                #k=700 are folded domains!
                if not bond.attrib["k"] == "700":
                    p1 = bond.attrib["p1"]
                    p2 = bond.attrib["p2"]
                    yield p1, p2

def bonds_from_pdb(filename):
    #Generate bond info iterator from pdb (kinda deprecated)
    warnings.warn("Be cautios if your Molecules are not line shaped. Tree like structures could lead to problems!")
    atom_index = -1
    last_resid = 1000 #some index >0
    with open(filename) as inp:
        for line in inp:
            split = line.split()
            if split[0] == "ATOM":
                resid = int(split[5])
                atom_index += 1
                if resid == last_resid+1:
                    #if this is a bond atom
                    yield atom_index-1, atom_index
                last_resid = resid
    
def bonds_from_bondsTXT(filename):
    data = np.loadtxt(filename, skiprows = 1, usecols=[0,1], dtype = int)
    return data[:,:2]
            
def gen_tcl_script(iterator):
    #takes the iterator and formats its output to tcl script
    output_file = """set blist {}
    """
    entry_string = lambda p1, p2: f"lappend blist [list {p1} {p2} A-A]\n"
    for p1, p2 in iterator:
        output_file += entry_string(p1, p2)

    output_file += "topo setbondlist type $blist"
    return output_file

def write_tcl_file(output_file, TCL_script):
    #actually writes an tcl script
    with open(output_file, "w") as w:
        w.write(TCL_script)

if __name__ == "__main__":
    #parser IO
    parser = argparse.ArgumentParser(
                        prog='TCL-Generator for Calvados',
                        description='Takes a calvados pdb or xml file and generates a TCL sctipt to tell VMD which Atoms are bond. You can use it via positional arguments or via tags.',
                        epilog='END')
    parser.add_argument("-i", "--inputfile",
                        default=None,
                        help = "Tag defined input file,",
                        required = True)
    parser.add_argument("-o", "--outputfile",
                        default = "bonds.tcl",
                        help = "Tag defined output file.",
                        required = False)
    args = parser.parse_args()

    input_file = args.inputfile
    output_file = args.outputfile
    #bondTXT_pattern = re.compile("bonds_?*.txt")
    inp_suffix = input_file.split(".")[-1]
    #if bondTXT_pattern.match(input_file):
    #    iterator = bonds_from_bondsTXT(input_file)
    if inp_suffix == "xml":
        iterator = bonds_from_xml(input_file)
    elif inp_suffix == "pdb":
        #works only if all molecules have resids 0 to N
        iterator = bonds_from_pdb(input_file)
    else:
        raise ValueError(f"Datatype of input file {input_file} unknown!")
    
    script = gen_tcl_script(iterator)
    write_tcl_file(output_file, script)




