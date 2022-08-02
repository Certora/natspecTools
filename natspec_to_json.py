import argparse
import json
import logging
import os
import re
import sys
from collections import OrderedDict
from typing import Any, Dict, List, Tuple, Optional, Set, BinaryIO
from pathlib import Path
import natspec_parser


def natspec_to_json(args: List[str]) -> None:
    """
    This is the main function of generating natpec information.
    the function is getting as an input a file and generating a Json !
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='specify a name of input spec file ', type=str)
    parser.add_argument('-v', '--verbosity', help='increase output verbosity', action='store_true')
    parser.add_argument('-dev', '--development', help='produce developer report', action='store_true')
    parser.add_argument('-user', '--user', help='produce end user report', action='store_true')
    args_used = parser.parse_args()
    if args_used.verbosity:
        print(f'input file is: {args_used.input_file}')

    documentations = natspec_parser.parse([args_used.input_file])

    print(documentations)

    json_string = json.dumps(documentations.__dict__)

    json_file = open('data.json', 'w')
    json_file.write(json_string)
    json_file.close()


if __name__ == '__main__':
    natspec_to_json(sys.argv[1:])
