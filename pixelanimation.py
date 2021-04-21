import inkex
import sys
import subprocess

class PixelAnimation(inkex.EffectExtension):
    def effect(self):
        #print("hello! ", args.input_file, file=sys.stderr)
        args = self.arg_parser.parse_args()
        filename = args.input_file
        sysPython = r"C:\Users\Julia\AppData\Local\Programs\Python\Python39\python.exe"

        if (args.radio == "export"):
            pyFile = r"C:\Users\Julia\AppData\Roaming\inkscape\extensions\svg_process.py"
            subprocess.run([sysPython, pyFile, filename, str(args.colors), str(args.output_size)], stderr=sys.stderr)
        else:
            pyFile = r"C:\Users\Julia\AppData\Roaming\inkscape\extensions\animation.py"
            subprocess.run([sysPython, pyFile, str(args.anim_speed)], stderr=sys.stderr)

    def add_arguments(self, pars):
        pars.add_argument("--radio", type=str)
        pars.add_argument("--colors", type=int)
        pars.add_argument("--output_size", type=int)
        pars.add_argument("--anim_speed", type=int)

if __name__ == '__main__':
    PixelAnimation().run()
