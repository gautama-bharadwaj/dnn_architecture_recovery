from numpy import zeros
from known_dnn_models import densenet121, densenet169, densenet201, inception_resnet, inception_v3, mobilenetv1, mobilenetv2, vgg16, vgg19, xception
from functions import format_data, visualization
import os
import subprocess
from multiprocessing import Process
import argparse
import sys
from datetime import date
import csv


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
        optional_args = parser.add_argument_group("Optional Arguments")
        mandatory_args.add_argument(
            "-m", "--model", type=str, required=True, help="Enter the model to perform analysis on"
        )
        mandatory_args.add_argument(
            "-i", "--iterations", type=int, required=True, help="Enter the number of iterations"
        )
        optional_args.add_argument(
            "-v", "--visualize", type=bool, required=False, help="Visualize the last executed model"
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
            model=args.model,
            iterations=args.iterations,
            visualize = args.visualize
        ).items()

def perf_measurement(file_path):
    print("Perf called: \n")
    subprocess.call("perf stat -e cycles,branches,instructions,cache-references,cache-misses,bus-cycles,branch-loads,iTLB-load-misses,dTLB-load-misses -p " +
                    str(os.getpid())+" -I 10 --output raw_output/"+file_path+".txt &", shell=True)
    getattr(sys.modules[__name__], file_path).run_model()

def repeated_runs(keyword_args, n, visualize):
    max_lines = 0
    for i in range(0, n):
        file = keyword_args['model']+".py"
        if not os.path.exists("known_dnn_models/"+file):
            print("The model "+file+" does not exist. Please enter the right argument")
            exit()
        p = Process(target=perf_measurement, args=(keyword_args['model'],))
        p.start()
        p.join()
        line_count = format_data.write_to_csv(keyword_args['model']+"-"+str(i))
        if (line_count>max_lines):
            max_lines = line_count

    if (visualize):
        visualization.graph_plotting('output/'+keyword_args['model']+'-'+str(i)+'.csv')
    for i in range(0, n):
        lis = list(csv.reader(open('output/'+keyword_args['model']+'-'+str(i)+'.csv')))
        final_time_stamp = lis[-1][0]
        cols = len(lis[-1])
        row_count = len(lis)
        zero_append_list = [0]*cols
        if (row_count < max_lines):
            csv_file = open('output/'+keyword_args['model']+'-'+str(i)+'.csv', 'a', encoding='UTF8')
            writer = csv.writer(csv_file)
            extra_row = 1
            for i in range(row_count, max_lines):
                time_inc = str(float(final_time_stamp) + 0.01*extra_row)
                zero_append_list[0] = time_inc
                writer.writerow(zero_append_list)
                extra_row += 1


# def append_zeros(keyword_args, n):


if __name__ == '__main__':
    keyword_args = dict(Parser().get_kwargs())
    repeated_runs(keyword_args, keyword_args['iterations'], keyword_args['visualize'])


