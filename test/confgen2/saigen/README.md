# saigen - dash config generator for SAI objects
* Based on `dashgen` modules
* Uses inheritance, reuses most methods
* Mostly just override renderItem() method to transform `dashgen` data structures into `SAI` structures prior to JSON seialization
* Initially showcase `eni` and `aclgroups` to demonstrate techniques.

# Example

Help for generate all:
```
$ ./generate.s.py -h
usage: generate.s.py [-h] [-f {json}] [-c {dict,list}] [-d] [-m] [-M "MSG"] [-n] [-P "{PARAMS}"] [-p PARAM_FILE]
                     [-o OFILE] [-s] [-S] [-v]

Generate DASH Configs

optional arguments:
  -h, --help            show this help message and exit
  -f {json}, --format {json}
                        Config output format.
  -c {dict,list}, --content {dict,list}
                        Emit dictionary (with inner lists), or list items only
  -d, --dump-params     Just dump parameters (defaults with user-defined merged in
  -m, --meta            Include metadata in output (only if "-c dict" used)
  -M "MSG", --msg "MSG"
                        Put MSG in metadata (only if "-m" used)
  -n, --no-output       Write output to /dev/null (overrides -o); still print optional diagnostics
  -P "{PARAMS}", --set-params "{PARAMS}"
                        use parameter dict from cmdline, partial is OK; overrides defaults & from file
  -p PARAM_FILE, --param-file PARAM_FILE
                        use parameter dict from file, partial is OK; overrides defaults
  -o OFILE, --output OFILE
                        Output file (default: standard output)
  -s, --summary-stats   show summary stats at end)
  -S, --detailed-stats  show detailed stats throughout operation)
  -v, --verbose         show detailed messages throughout operation)

Usage
=========
./generate.s.py                - generate output to stdout using uber-generator
./generate.s.py -o tmp.json    - generate output to file tmp.json
./generate.s.py -o /dev/null   - generate output to nowhere (good for testing)
./generate.s.py -c list        - generate just the list items w/o parent dictionary
dashgen/aclgroups.py [options] - run one sub-generator, e.g. acls, routetables, etc.
                               - many different subgenerators available, support same options as uber-generator

Passing parameters. Provided as Python dict, see dflt_params.py for available items
Can use defaults; override from file; override again from cmdline (all 3 sources merged).
================
./generate.s.py -d                          - display default parameters and quit
./generate.s.py -d -P PARAMS                - use given parameters, display and quit; see dflt_params.py for template
./generate.s.py -d -p PARAM_FILE            - override with parameters from file; display only
./generate.s.py -d -p PARAM_FILE -P PARAMS  - override with params from file and cmdline; display only
./generate.s.py -p PARAM_FILE -P PARAMS     - override with params from file and cmdline; generate output

Diagnostic Options:
===================
./generate.s.py -v              - display verbose progress messages
./generate.s.py -S              - display verbose stats (#items, memory usage) throughout
./generate.s.py -ns             - suppress output, just display summary geneator stats at end
./generate.s.py -nsSv           - suppress output, display all diagnostics and summary stats at end

Misc. Examples:
===============
./generate.s.py -d -p params_small.py -P "{'ENI_COUNT': 16}"  - use params_small.py but override ENI_COUNT; display params
./generate.s.py -p params_hero.py -o tmp.json                 - generate full "hero test" scale config as json file
./dashgen/vpcmappingtypes.py -m -M "Kewl Config!"             - generate dict of vpcmappingtypes, include meta with message            
```
Help for generate aclgroups only:
```
$ ./saigen/aclgroups_sai.py -h
usage: aclgroups_sai.py [-h] [-f {json}] [-c {dict,list}] [-d] [-m] [-M "MSG"] [-n] [-P "{PARAMS}"]
                        [-p PARAM_FILE] [-o OFILE] [-s] [-S] [-v] [-a] [-e ENI_INDEX] [-t TABLE_INDEX]

Generate DASH Configs

optional arguments:
  -h, --help            show this help message and exit
  -f {json}, --format {json}
                        Config output format.
  -c {dict,list}, --content {dict,list}
                        Emit dictionary (with inner lists), or list items only
  -d, --dump-params     Just dump parameters (defaults with user-defined merged in
  -m, --meta            Include metadata in output (only if "-c dict" used)
  -M "MSG", --msg "MSG"
                        Put MSG in metadata (only if "-m" used)
  -n, --no-output       Write output to /dev/null (overrides -o); still print optional diagnostics
  -P "{PARAMS}", --set-params "{PARAMS}"
                        use parameter dict from cmdline, partial is OK; overrides defaults & from file
  -p PARAM_FILE, --param-file PARAM_FILE
                        use parameter dict from file, partial is OK; overrides defaults
  -o OFILE, --output OFILE
                        Output file (default: standard output)
  -s, --summary-stats   show summary stats at end)
  -S, --detailed-stats  show detailed stats throughout operation)
  -v, --verbose         show detailed messages throughout operation)
  -a, --acls-ipv4       Generate IPv4 ACL group tables, suppress top-level container
  -e ENI_INDEX, --eni-index ENI_INDEX
                        Specify single ENI index (use with -a option only)
  -t TABLE_INDEX, --table-index TABLE_INDEX
                        Specify single table index (use with -a option only)

Usage
=========
./saigen/aclgroups_sai.py                - generate output to stdout using uber-generator
./saigen/aclgroups_sai.py -o tmp.json    - generate output to file tmp.json
./saigen/aclgroups_sai.py -o /dev/null   - generate output to nowhere (good for testing)
./saigen/aclgroups_sai.py -c list        - generate just the list items w/o parent dictionary
dashgen/aclgroups.py [options] - run one sub-generator, e.g. acls, routetables, etc.
                               - many different subgenerators available, support same options as uber-generator

Passing parameters. Provided as Python dict, see dflt_params.py for available items
Can use defaults; override from file; override again from cmdline (all 3 sources merged).
================
./saigen/aclgroups_sai.py -d                          - display default parameters and quit
./saigen/aclgroups_sai.py -d -P PARAMS                - use given parameters, display and quit; see dflt_params.py for template
./saigen/aclgroups_sai.py -d -p PARAM_FILE            - override with parameters from file; display only
./saigen/aclgroups_sai.py -d -p PARAM_FILE -P PARAMS  - override with params from file and cmdline; display only
./saigen/aclgroups_sai.py -p PARAM_FILE -P PARAMS     - override with params from file and cmdline; generate output

Diagnostic Options:
===================
./saigen/aclgroups_sai.py -v              - display verbose progress messages
./saigen/aclgroups_sai.py -S              - display verbose stats (#items, memory usage) throughout
./saigen/aclgroups_sai.py -ns             - suppress output, just display summary geneator stats at end
./saigen/aclgroups_sai.py -nsSv           - suppress output, display all diagnostics and summary stats at end

Misc. Examples:
===============
./saigen/aclgroups_sai.py -d -p params_small.py -P "{'ENI_COUNT': 16}"  - use params_small.py but override ENI_COUNT; display params
./saigen/aclgroups_sai.py -p params_hero.py -o tmp.json                 - generate full "hero test" scale config as json file
./dashgen/vpcmappingtypes.py -m -M "Kewl Config!"             - generate dict of vpcmappingtypes, include meta with message            

ACL Group-specific Examples:
============================
NOTE: Effective ACL group = (eni_index * 1000 + table_index).

The -a option allows you to generate rules only (no GROUP container) for one ENI/ACL group.
Use repeatedly if you need more instances, or write a custom program for other options.
Omit -a to generate entire ACL groups config per input PARAMs.
The output from -a option will NOT have an enclosing container with ACL group but the IP addresses,
etc. will correspond to the ACL group rules obtained using the normal "full output" (no -a option).

./dashgen/aclgroups.py [-p PARAM_FILE] [-P PARAMS]       - generate ACL entries and group container using PARAMs from global options
./dashgen/aclgroups.py -a                                - generate ACL rules only for ENI=1 Group=1001
./dashgen/aclgroups.py -a -e 3 -t 2                      - generate ACL rules only for ENI=3 Group=3002
```

Generate all:
```
{
  "enis":
[
  {
    "eni_id": {
      "type": "SAI_OBJECT_TYPE_ENI",
      "attributes": {
        "SAI_ENI_ATTR_CPS": "10000",
        "SAI_ENI_ATTR_PPS": "100000",
        "SAI_ENI_ATTR_FLOWS": "100000",
        "SAI_ENI_ATTR_ADMIN_STATE": "True",
        "SAI_ENI_ATTR_VM_UNDERLAY_DIP": "vm_underlay_dip",
        "SAI_ENI_ATTR_VM_VNI": "9",
        "SAI_ENI_ATTR_VNET_ID": "self.vnet_id",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE5_DASH_ACL_GROUP_ID": "$placeholder"
      }
    }
  },
  {
    "eni_id": {
      "type": "SAI_OBJECT_TYPE_ENI",
      "attributes": {
        "SAI_ENI_ATTR_CPS": "10000",
        "SAI_ENI_ATTR_PPS": "100000",
        "SAI_ENI_ATTR_FLOWS": "100000",
        "SAI_ENI_ATTR_ADMIN_STATE": "True",
        "SAI_ENI_ATTR_VM_UNDERLAY_DIP": "vm_underlay_dip",
        "SAI_ENI_ATTR_VM_VNI": "9",
        "SAI_ENI_ATTR_VNET_ID": "self.vnet_id",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V4_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_INBOUND_V6_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V4_STAGE5_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE1_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE2_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE3_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE4_DASH_ACL_GROUP_ID": "$placeholder",
        "SAI_ENI_ATTR_OUTBOUND_V6_STAGE5_DASH_ACL_GROUP_ID": "$placeholder"
      }
    }
  }
],
  "acl-groups":
[
  {
    "ACL-GROUP:ENI:1:TABLE:1001": {
      "acl-group-id": "acl-group-1001",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:1:TABLE:1002": {
      "acl-group-id": "acl-group-1002",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:1:TABLE:1003": {
      "acl-group-id": "acl-group-1003",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:1:TABLE:1004": {
      "acl-group-id": "acl-group-1004",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:1:TABLE:1005": {
      "acl-group-id": "acl-group-1005",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:1:TABLE:1006": {
      "acl-group-id": "acl-group-1006",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-1006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "1.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2001": {
      "acl-group-id": "acl-group-2001",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.128.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2001",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2002": {
      "acl-group-id": "acl-group-2002",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.132.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2002",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2003": {
      "acl-group-id": "acl-group-2003",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.136.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2003",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2004": {
      "acl-group-id": "acl-group-2004",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.140.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2004",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2005": {
      "acl-group-id": "acl-group-2005",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.144.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2005",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  },
  {
    "ACL-GROUP:ENI:2:TABLE:2006": {
      "acl-group-id": "acl-group-2006",
      "ip_version": "IPv4",
      "rules": [
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.148.0.3/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        },
        {
          "type": "SAI_OBJECT_TYPE_DASH_ACL_RULE",
          "attributes": {
            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID": "acl-group-2006",
            "SAI_DASH_ACL_RULE_ATTR_PRIORITY": 1,
            "SAI_DASH_ACL_RULE_ATTR_ACTION": "SAI_DASH_ACL_RULE_ACTION_DENY",
            "SAI_DASH_ACL_RULE_ATTR_DIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_SIP": "2.1.0.1/32",
            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_DST_PORT": "TBD - optional?",
            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID": "TODO"
          }
        }
      ]
    }
  }
]
}
```