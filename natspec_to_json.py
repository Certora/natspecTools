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


def natspec_to_json(args) -> None:
    """
    This is the main function of generating natspec information.
    the function is getting as an input a file and generating a Json !
    """
    if args.verbosity:
        print(f'input file(s) : {args.input_file}')

    # The parse function returns a list of documentations list, one
    # list for each input file.
    files_documentations = natspec_parser.parse(args.input_file)

    # loop through all documentation lists.
    file_number = 0
    for documentation_list in files_documentations:
        if args.verbosity:
            print(f'processing file no: {args.input_file[file_number]}')

        json_object_list = handle_documentation_list(documentation_list)

        # build output file name from input file name
        input_filename, file_extension = os.path.splitext(args.input_file[file_number])
        output_filename = os.path.join(input_filename + '-natspec' + '.json')

        json_string = json.dumps(json_object_list, indent=4)
        json_file = open(output_filename, 'w')
        json_file.write(json_string)
        json_file.close()
        file_number += 1

    if args.verbosity:
        print('processing finished!')

def handle_documentation_list(documentation_list) -> List[Dict]:
    document_dicts = []
    for documentation in documentation_list:
        result_data = handle_documentation(documentation)
        if result_data is not None:
            document_dicts.append(result_data)

    return document_dicts


# handle documentation
# a documentation can be a 'Free form' or an actual 'Documentation' object
def handle_documentation(documentation) -> Dict[str, any]:
    doc_dict = {}
    diagnostics = documentation.diagnostics()

    # display all documentation diagnostic messages, if exist
    for message in diagnostics:
        print_diag(message)

    # check if this item is a FreeForm text
    if documentation.__class__.__name__ == 'FreeForm':
        doc_dict['type'] = 'text'
        doc_dict['header'] = documentation.header
        doc_dict['text'] = documentation.block
        return doc_dict
    elif documentation.__class__.__name__ == 'Documentation':  # Documentation object
        if documentation.associated is not None:
            doc_dict['content'] = documentation.associated.block
            function_names = ['function', 'definition', 'ghost variable', 'ghost function']
            other_names = ['summerization', 'import', 'use', 'using', 'hook']

            if documentation.associated.kind in function_names:
                doc_dict['type'] = 'function'
            elif documentation.associated.kind == 'rule':
                doc_dict['type'] = 'rule'
            elif documentation.associated.kind == 'invariant':
                doc_dict['type'] = 'invariant'
            elif documentation.associated.kind in other_names:
                doc_dict['type'] = documentation.associated.kind
            else:
                print(f'unknown element type : {documentation.associated.kind}')

            # add parameters info, if exist
            param_list = []
            param_index = 0
            for param in documentation.associated.params:
                param_dict = {'type': param[0], 'name': param[1]}
                param_list.append(param_dict)

            doc_dict['params'] = param_list

            # get the return data type
            ret_data = {}
            if documentation.associated.returns is not None:
                ret_data = {'type': documentation.associated.returns}
            else:
                ret_data = {'type': 'None'}
            doc_dict['return'] = ret_data

        else:  # associated element is unrecognized.
            doc_dict['type'] = 'unknown'

    else:
        print('NatSpec parser library type is not supported!')
        return None

    for doc_tag in documentation.tags:
        handle_tag(doc_dict, doc_tag)

    return doc_dict


def get_parser():
    # separate the argument parser definition
    parser = argparse.ArgumentParser(description='export Natspec comments to JSON file(s)',
                                     epilog='please, use with care')
    parser.add_argument('input_file', help='specify a name of input spec file ', type=str, nargs='+')
    parser.add_argument('-v', '--verbosity', help='increase output verbosity', action='store_true')
    parser.add_argument('-dev', '--development', help='produce developer report', action='store_true')
    parser.add_argument('-user', '--user', help='produce end user report', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s Ver 0.1')
    return parser


def print_diag(diagnostic):
    diag_msg = ''

    if diagnostic.severity == diagnostic.severity.Error:
        diag_msg += '*** Error! '
    elif diagnostic.severity == diagnostic.severity.Warning:
        diag_msg += 'Warning: '
    else:  # TODO
        diag_msg += 'Info: '

    diag_msg += f'line:  {diagnostic.range.start.line} Col: {diagnostic.range.start.character}: '
    diag_msg += diagnostic.description
    print(diag_msg)


# handle documentation tags
def handle_tag(doc_dict, tag):
    if tag.kind == 'title':
        doc_dict['title'] = tag.description
    elif tag.kind == 'notice':
        doc_dict['notice'] = tag.description
    elif tag.kind == 'formula':
        doc_dict['formula'] = tag.description
    elif tag.kind == 'return':
        ret_data = doc_dict['return']
        ret_data['comment'] = tag.description
    elif tag.kind == 'param':
        param_name_match = re.match(r"^\w+", tag.description)
        if param_name_match:
            # get the param name from the comment
            # find it in the param lists, and
            param_name = param_name_match.group()
            params_info_list = doc_dict['params']
            for param_info in params_info_list:
                if param_info['name'] == param_name:
                    param_info['comment'] = tag.description
    else:
        print(f'unsupported tag: {tag.kind}')


VERSION_STR = '0.0.1'
if __name__ == '__main__':
    __version__ = VERSION_STR
    parser = get_parser()
    args = parser.parse_args()
    natspec_to_json(args)
