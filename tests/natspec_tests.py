import json
import src.CVLDoc.natspec_to_json as natspec_to_json
from deepdiff import DeepDiff
from pprint import pprint
from pathlib import Path
import os

#test_args = ['-v']
#filenames = ['basic_tests\\function_test.spec',
#             'basic_tests\\invariant_test.spec',
#             'test\\rules_test.spec',
#             'test\\import_test.spec',
#             'test\\methods_test.spec',
#             'test\\use_test.spec',
#             'test\\using_test.spec',
#             'test\\full_contract.spec']

# parser = natspec_to_json.get_parser()
# args = parser.parse_args(test_args + filenames)
# natspec_to_json.natspec_to_json(args)

# rnu a single test file




def run_test_file(filename):
    test_args = ['-v', filename]

    parser = natspec_to_json.get_parser()
    args = parser.parse_args(test_args)
    natspec_to_json.natspec_to_json(args)
    input_filename, file_extension = os.path.splitext(filename)
    output_filename = os.path.join(input_filename + '-natspec' + '.json')
    expected_filename = os.path.join(input_filename + '-expected' + '.json')
    file_output = open(output_filename)
    file_expected = open(expected_filename)
    output_data = json.load(file_output)
    expected_data = json.load(file_expected)
    diff = DeepDiff(output_data, expected_data, )
    return diff


def test_full_contract():
    diff = run_test_file(str(Path('basic_tests/full_contract.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_invariant():
    diff = run_test_file(str(Path('basic_tests/invariant_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_function():
    diff = run_test_file(str(Path('basic_tests/function_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_rules():
    diff = run_test_file(str(Path('basic_tests/rules_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_methods():
    diff = run_test_file(str(Path('basic_tests/methods_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_using():
    diff = run_test_file(str(Path('basic_tests/using_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0
def test_import():
    diff = run_test_file(str(Path('basic_tests/import_test.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0

def test_burnable():

    diff = run_test_file(str(Path('customer_code/ERC1155Burnable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_new():

    diff = run_test_file(str(Path('customer_code/ERC1155New.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_pausable():
    diff = run_test_file(str(Path('customer_code/ERC1155Pausable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_supply():
    diff = run_test_file(str(Path('customer_code/ERC1155Supply.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_governor():
    diff = run_test_file(str(Path('customer_code/GovernorPreventLateQuorum.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


def test_initializable():
    diff = run_test_file(str(Path('customer_code/Initializable.spec')))
    if diff:
        pprint(diff, indent=4)
        assert 0


if __name__ == '__main__':
    # perform basic tests
    test_function()
    test_invariant()
    test_rules()
    test_import()
    test_using()
    test_full_contract()

    # advanced tests
    test_burnable()
    test_new()
    test_pausable()
    test_supply()
    test_governor()
    test_initializable()
