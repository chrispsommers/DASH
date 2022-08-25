#!/usr/bin/python3
#
# REad in tmp.json created by confgen2, emit file using orjson technique 
# per confgen so text can be compared to  ensure algorithm fidelity despite refactorings
import json
import orjson
import argparse, textwrap

parser = argparse.ArgumentParser(description='Reformat JSON using orjson for strict text comparisons',
                formatter_class=argparse.RawTextHelpFormatter,
                epilog = textwrap.dedent('''
Example:
========
orj_rfmt -i tmp1.json -o tmp1.or.json
                '''))

parser.add_argument(
        '-i', '--input', default='dash_conf.json', metavar='IFILE',
        help="Input file (default: dash_conf.json)")

parser.add_argument(
        '-o', '--output', default='dash_conf.or.json', metavar='OFILE',
        help="Output file (default: dash_conf.or.json)")

args = parser.parse_args()

print("Reading %s..." % args.input)
with open(args.input, 'r') as fpr:
    d=json.load(fpr)

print("Writing %s..." % args.output)

with open(args.output, 'wb') as fpw:
    fpw.write(orjson.dumps(d, option=orjson.OPT_INDENT_2))


