import argparse
from PyLabControl.src.tools.export_default import export
from PyLabControl.src.gui.run_gui import run_gui

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--export", nargs='+', help ="exports default instrumets, probes, and scripts\n  \
                                                           call PyLabControl target_folder source_folders(optional) class_type(optional) \
                                                           target_folder:\t target folder where to export .b26 files \
                                                           source_folder:\t source folder with location of .python files from which to create .b26 files \n \
                                                           \t\t can also be the name of a package that contains the python files (e.g. b26tool_kit) \n \
                                                           \t\t if empty export from PyLabControl \n \
                                                           class_type:\t type of class to export as .b26 file (intrument, script, probe or all) \
                                                           ")
    parser.add_argument("-g", "--gui", nargs='?', const = '', type = str, help="loads the default gui")
    args = parser.parse_args()

    if args.export is not None:

        if len(args.export) == 1:
            target_folder = args.export[0]
            export(target_folder)
        elif len(args.export) == 2:
            target_folder = args.export[0]
            source_folder = args.export[1]
            export(target_folder, source_folder)
        elif len(args.export) == 3:
            target_folder = args.export[0]
            source_folder = args.export[1]
            class_type = args.export[2]

            export(target_folder, source_folder, class_type)
        else:
            parser.error('The -e or --export keyword must be given one to three arguments')
            parser.print_help()
    elif args.gui is not None:

        fname = args.gui
        run_gui(fname)
    else:
        parser.print_help()