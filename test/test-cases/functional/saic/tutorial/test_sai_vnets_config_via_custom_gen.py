#!/usr/bin/python3
# Demonstration of how to generate many config objects with a custom generator
# Run as pytest or standalone script:
# - as a Pytest, run using the appropriate SAI Challenger setup file, e.g:
#      pytest -sv --setup ../sai_dpu_client_server_snappi.json .
#
# - in standalone mode, use to generate JSON to stdout, which can be saved to a file
#    content into a test-case. Example:
#    python3 <this-filename> [options]  (use -h for help)

import json
import sys
from pprint import pprint
import argparse

import pytest

# Constants
SWITCH_ID = 5

# create vnets
def make_create_cmds():
    """ Return some configuration entries using custom generator"""
    for x in range(1,101):
        yield \
            {
                "name": "vnet%d" % x,
                "op": "create",
                "type": "SAI_OBJECT_TYPE_VNET",
                "attributes": [
                    "SAI_VNET_ATTR_VNI",
                    "%d" % (x + 2000)
                ]
            } 
    

def make_remove_cmds():
    """ Return an array of remove commands """
    cleanup_commands = [{'name': cmd['name'], 'op': 'remove'} for cmd in make_create_cmds()]
    for cmd in reversed(cleanup_commands):
        yield cmd
    return

class TestSaiDashVnetsGenerator:
    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vnets_create_via_generator(self, dpu):
        """Verify configuration create
        """
        results = [*dpu.process_commands( (make_create_cmds()) )]
        print("\n======= SAI commands RETURN values =======")
        pprint(results)
        assert all(results), "Create error"

    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vnets_remove_via_generator(self, dpu):
        """Verify configuration removal
        """
        results = [*dpu.process_commands(make_remove_cmds())]
        print("\n======= SAI commands RETURN values =======")
        assert all( [result == 0 for result in results]), "Remove error"
        print(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DASH SAI Config Generator for vnet table entries')
    parser.add_argument('-a', action='store_true', help='Generate ALL commands as JSON to stdout')
    parser.add_argument('-c', action='store_true', help='Generate CREATE commands as JSON to stdout')
    parser.add_argument('-r', action='store_true', help='Generate REMOVE commands as JSON to stdout')

    args = parser.parse_args()

    if not args.a and not args.c and not args.r:
        # must provide at least one flag
        print ("\n*** Please specify at least one option flag from [acr] to generate output ***\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.a or args.c:
        print(json.dumps([item for item in make_create_cmds()],
                         indent=2))

    if args.a or args.r:
        print (json.dumps([item for item in make_remove_cmds()],
                         indent=2)) 

