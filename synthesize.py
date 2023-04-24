#!/usr/bin/env python

import subprocess
import argparse

# source file, output file, and top level module name are all command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("source_file", type=str, help="path to the source file")
parser.add_argument("module_name", type=str, help="name of the top-level module")
parser.add_argument("--output_file","-o", type=str, help="path to the output file, without extension")
args=parser.parse_args()

# Define the source file name and output file name
source_file = args.source_file

if(args.output_file):
    # if output file is given, use that.  splits on . to ensure no extension.  Will not handle hidden files that start with .
    output_file = args.output_file
    splitstr = output_file.split(".")
    loc = output_file.find(".")
    output_file = splitstr[0]
    if(loc == 0):
        raise NotImplementedError("Script does not support the output file being a hidden file")

else:
    output_file = "./schematic"

module_name = args.module_name

# yosys -p "read_verilog decoder1to2.sv; synth -top decoder1to2; show -prefix ./schematic.png -colors 1 -format png"

# Synthesize the circuit using Yosys
yosys_script = f"read_verilog -sv {source_file}; synth -top {module_name}; proc; opt; show -prefix {output_file} -colors 2 -format png"
yosys_process = subprocess.Popen(["yosys", "-p", yosys_script], stdout=subprocess.PIPE)
yosys_output, yosys_error = yosys_process.communicate()

# Check for errors during synthesis
if yosys_error is not None:
    print(f"Yosys error: {yosys_error.decode()}")
else:
    print(f"Synthesis successful! Circuit exported as {output_file}")
