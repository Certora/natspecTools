import json
import natspec_to_json
from deepdiff import DeepDiff
from pprint import pprint

import os

filenames = ['Test\\function_test.spec',
             'Test\\invariant_test.spec',
             'test\\rules_test.spec',
             'test\\import_test.spec',
             'test\\methods_test.spec',
             'test\\use_test.spec',
             'test\\using_test.spec',
             'test\\full_contract.spec']

parser = natspec_to_json.get_parser()
args = parser.parse_args(filenames)
natspec_to_json.natspec_to_json(args)

# check the result against the expected results
for filename in filenames:
    input_filename, file_extension = os.path.splitext(filename)
    output_filename = os.path.join(input_filename + '-natspec' + '.json')
    expected_filename = os.path.join(input_filename + '-expected' + '.json')
    file_output = open(output_filename)
    file_expected = open(expected_filename)

    output_data = json.load(file_output)
    expected_data = json.load(file_expected)

    diff = DeepDiff(output_data, expected_data, )

    print(f'Checking test results for file: {filename}')
    if diff:
        print('Test failed:')
        pprint(diff, indent=4)
    else:
        print("Test Passed")



