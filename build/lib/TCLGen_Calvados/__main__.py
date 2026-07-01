import argparse
from .subroutines import search_for_file, bonds_from_bondsTXT, bonds_from_pdb, bonds_from_xml, gen_tcl_script, write_tcl_file

def main():
    #parser IO
    parser = argparse.ArgumentParser(
                        prog='TCL-Generator for Calvados',
                        description='Takes a calvados pdb or xml file and generates a TCL sctipt to tell VMD which Atoms are bond. You can use it via positional arguments or via tags.',
                        epilog='END')
    parser.add_argument("-i", "--inputfile",
                        default=None,
                        help = "Tag defined input file,",
                        required = False)
    parser.add_argument("-o", "--outputfile",
                        default = "bonds.tcl",
                        help = "Tag defined output file.",
                        required = False)
    args = parser.parse_args()

    if args.inputfile is None:
        input_file = search_for_file("xml")
    else:
        input_file = args.inputfile
    output_file = args.outputfile
    #bondTXT_pattern = re.compile("bonds_?*.txt")
    inp_suffix = input_file.split(".")[-1]
    #if bondTXT_pattern.match(input_file):
    #    
    
    if inp_suffix == "xml":
        iterator = bonds_from_xml(input_file)
    elif inp_suffix == "pdb":
        #works only if all molecules have resids 0 to N
        iterator = bonds_from_pdb(input_file)
    elif inp_suffix == "txt":
        iterator = bonds_from_bondsTXT(input_file)
    else:
        raise ValueError(f"Datatype of input file {input_file} unknown!")
    
    script = gen_tcl_script(iterator)
    write_tcl_file(output_file, script)

if __name__ == "__main__":
    main()