import argparse
import os
from util import util

class BaseOptions():
    """This class defines options used during both training and test time.

    It also implements several helper functions such as parsing, printing, and saving the options.
    It also gathers additional options defined in <modify_commandline_options> functions in both dataset class and model class.
    """

    def __init__(self):
        """Reset the class; indicates the class hasn't been initailized"""
        self.initialized = False

    def initialize(self, parser):
        """Define the common options that are used in both training and test."""
        # basic parameters
        parser.add_argument('--dataroot', required=True, help='path to video or directory of videos to process')
        parser.add_argument('--output', required=True, help='path to output directory')
        parser.add_argument('--isDirectory', action='store_true', help='if dataroot is a directory or not')
        parser.add_argument('--shotcount', type=int, default=24, help='# images to export')
        parser.add_argument('--dimensionx', type=int, default=24, help='x dimension to scale the input video to before cropping')
        parser.add_argument('--dimensiony', type=int, default=24, help='y dimension to scale the input video to before cropping')
        parser.add_argument('--cropx', type=int, default=24, help='crop x dimension for final output')
        parser.add_argument('--cropy', type=int, default=24, help='crop y dimension for final output')
        parser.add_argument('--randomCrop', action='store_true', help='if the clipper should randomly crop instead of being in the middle')
        parser.add_argument('--randomClip', action='store_true', help='get random frames instead of a straight frame sequence')
        parser.add_argument('--frameStart', type=int, default=-1, help='First frame of the video to use')
        parser.add_argument('--frameEnd', type=int, default=-1, help='last frame of the video to use')
        
        
        parser.add_argument('--extension', type=str, default='png', help='extension of files to process')
        parser.add_argument('--processType', type=str, default='crop', help='Process type to use: (crop, consolidate, zip)')
 
        self.initialized = True
        return parser
    
    def gather_options(self):
        """Initialize our parser with basic options(only once).
        Add additional model-specific and dataset-specific options.
        These options are defined in the <modify_commandline_options> function
        in model and dataset classes.
        """
        if not self.initialized:  # check if it has been initialized
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser)

        # get the basic options
        opt, _ = parser.parse_known_args()

        # save and return the parser
        self.parser = parser
        return parser.parse_args()
    
    
    def print_options(self, opt):
        """Print and save options

        It will print both current options and default values(if different).
        It will save options into a text file / [checkpoints_dir] / opt.txt
        """
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)

        # # save to the disk
        # expr_dir = os.path.join(opt.checkpoints_dir, opt.name)
        # util.mkdirs(expr_dir)
        # file_name = os.path.join(expr_dir, '{}_opt.txt'.format(opt.phase))
        # with open(file_name, 'wt') as opt_file:
        #     opt_file.write(message)
        #     opt_file.write('\n')

    def parse(self):
        """Parse our options, create checkpoints directory suffix, and set up gpu device."""
        opt = self.gather_options()
        self.print_options(opt)
        self.opt = opt
        return self.opt
