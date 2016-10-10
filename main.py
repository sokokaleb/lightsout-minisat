import argparse

from src.lights_out_minisat_wrapper import LightsOutMinisatWrapper
from src.lights_out_gui import LightsOutGUI

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='LightsOut! puzzle and solver implementation using Minisat.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--path',
            help='Path that will be used to store temporary files',
            default='/tmp',
            type=str)
    parser.add_argument('-c', '--command',
            help='Command to execute minisat program (e.g., \'minisat\', or \'./minisat\')',
            default='minisat',
            type=str)
    args = parser.parse_args()

    minisat_wrapper = LightsOutMinisatWrapper(
            exec_command=args.command,
            in_file_path='{0}/lightsout_in'.format(args.path),
            out_file_path='{0}/lightsout_out'.format(args.path),
            meta_file_path='{0}/lightsout_meta'.format(args.path))

    gui = LightsOutGUI(minisat_wrapper, 3, 3)
    gui.run()
