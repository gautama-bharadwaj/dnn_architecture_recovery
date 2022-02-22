from known_dnn_models import densenet121, densenet169, densenet201, inception_resnet, inception_v3, mobilenetv1, mobilenetv2, vgg16, vgg19, xception
from functions import format_data, visualization
import os
import subprocess
from multiprocessing import Process
import argparse
import sys
from datetime import date


class DefaultParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: {}\n".format(message))
        self.print_help()
        sys.exit(2)


class Parser:
    usage = "Generate performance report for DNN models specified by arguments"

    # noinspection PyTypeChecker
    def create_parser(self):
        parser = DefaultParser(
            description="%(prog)s",
            formatter_class=argparse.RawTextHelpFormatter,
            add_help=False,
            prog="DNN Architecture Recovery",
            usage=self.usage,
        )
        self.add_arguments(parser)
        return parser

    @staticmethod
    def add_arguments(parser):

        # Add optional options
        mandatory_args = parser.add_argument_group("Mandatory Arguments")
        mandatory_args.add_argument(
            "-m", "--model", type=str, required=True, help="Enter the model to perform analysis on"
        )
        help_ = parser.add_argument_group("help")
        help_.add_argument("-h", "--help", action="help",
                           help="Show usage info and exit")

    def get_kwargs(self):
        argv = sys.argv[1:] if sys.argv else ["--help"]
        count = 1
        for count, entry in enumerate(argv):
            if entry.startswith("-") or entry.startswith("--"):
                break
        parser = self.create_parser()
        args = parser.parse_args(argv[count:])

        # convert file formats to a list
        # args.file_format = [item for item in args.file_format.split(",")]

        return dict(
            model=args.model
        ).items()

def perf_measurement(file_path):
    print("Perf called: \n")
    subprocess.call("perf stat -e cycles,branches,instructions,cache-references,cache-misses,bus-cycles -p " +
                    str(os.getpid())+" -I 10 --output raw_output/"+file_path+".txt &", shell=True)
    getattr(sys.modules[__name__], file_path).run_model()


if __name__ == '__main__':
    keyword_args = dict(Parser().get_kwargs())
    file = keyword_args['model']+".py"
    if not os.path.exists("known_dnn_models/"+file):
        print("The model "+file+" does not exist. Please enter the right argument")
        exit()
    p = Process(target=perf_measurement, args=(keyword_args['model'],))
    p.start()
    p.join()
    format_data.write_to_csv(keyword_args['model'])
    visualization.graph_plotting('output/'+keyword_args['model']+'.csv')


