# Improved generator-based confgen
## Features
* Generate complex DASH configurations, parameter driven
* Custom input params
* Output to file or stdio
* Select output format: JSON, yaml (future), none
* Generate all config (uber-generator) or just selected items (e.g. aclgroups)
* Potential to create custom apps to transform streaming data e.g into device API calls w/o intermediate text rendering
## High-level Diagram

![confgen-hld-diag](confgen-hld-diag.svg)

## Design
The uber-generator `generate.d.py` instantiates sub-generators and produces a composite output stream which can be rendered into text files (JSON) or sent to stdout for custom pipelines.

The uber-generator and sub-generators all derive from a base-class `ConfBase`. They all share a common `main` progam with CLI command-line options, which allows them to be used independently yet consistently.

The generators produce Python data structures which can be rendered into output text (e.g. JSON) or used to feed custom applications such as a saithrift API driver, to directly configure a device. Likewise a custom API driver can be developed for vendor-specific APIs.

Default parameters allow easy operations with no complex input. All parameters can be selectively overridden via cmd-line, input file or both.

## Sample CLI Usage
This may not be current; check latest for actual content.
```
$ ./generate.d.py -h
usage: generate.d.py [-h] [-f {json}] [-c {dict,list}] [-d] [-m] [-M "MSG"] [-P "{PARAMS}"] [-p PARAM_FILE]
                     [-o OFILE]

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
  -P "{PARAMS}", --set-params "{PARAMS}"
                        supply parameters as a dict, partial is OK; defaults and file-provided (-p)
  -p PARAM_FILE, --param-file PARAM_FILE
                        use parameter dict from file, partial is OK; overrides defaults
  -o OFILE, --output OFILE
                        Output file (default: standard output)

Usage:
=========
./generate.d.py                - generate output to stdout using uber-generator
./generate.d.py -o tmp.json    - generate output to file tmp.json
./generate.d.py -o /dev/null   - generate output to nowhere (good for testing)
./generate.d.py -c list        - generate just the list items w/o parent dictionary
dashgen/aclgroups.py [options] - run one sub-generator, e.g. acls, routetables, etc.
                               - many different subgenerators available, support same options as uber-generator

Passing parameters. Provided as Python dict, see dflt_params.py for available items
================
./generate.d.py -d                          - display default parameters and quit
./generate.d.py -d -P PARAMS                - override given parameters, display and quit; see dflt_params.py for template
./generate.d.py -d -p PARAM_FILE            - override parameters in file; display only
./generate.d.py -d -p PARAM_FILE -P PARAMS  - override params from file, then override params from cmdline; display only
./generate.d.py -p PARAM_FILE -P PARAMS     - override params from file, then override params from cmdline, generate output

Examples:
./generate.d.py -d -p params_small.py -P "{'ENI_COUNT': 16}"  - use params_small.py but override ENI_COUNT; display params
./generate.d.py -p params_hero.py -o tmp.json                 - generate full "hero test" scale config as json file
dashgen/vpcmappingtypes.py -m -M "Kewl Config!"               - generate dict of vpcmappingtypes, include meta with message            
```
## Confgen Applications
Two anticipated applications (see Figure below):
* Generate a configuration file, e.g. JSON, and use this to feed downstream tools such as a DUT configuration utility.
* Use the output of the config data stream generators to perform on-the-fly DUT configuration without intermediate JSON file rendering; also configure traffic-generators using data in the config info itself.

![confgen-apps](confgen-apps.svg)

## SAI-Challenger Integration
The figure below depicts the integration of the *saigen* configuration generator and the SAI-Challenger pytest framework.
![saichallenger-enhanced](saichallenger-enhanced.svg)

The generator is one of several options to produce SAI (or possibly gNMI) configuration *records* which are applied to the DUT via one of several possible APIs, including saithrift, sairedis, gNMI, etc. The generator can provide streaming records which are translated on-the-fly into appropriate device API calls.

In addition, the generator can produce textual representations (e.g. JSON, YAML) of configuration records for usage as stored configurations which the framework can consume as test data input. Configuration files can be produced by other means including other scripts, text-editors, etc.

Finally, the framework can use literal configuration declarations represented as JSON, YAML, Python structures, etc. embedded directly into test-case code. This makes the most sense when the test cases are relatively simple.

Due to schema and/or semantic differences, a separate gNMI configuration generator might be preferred vs. translating the canonical SAI records into equivalent gNMI records for application to the gNMI interface.
![gnmigen](gnmigen.svg)

### Detailed saigen-Sai Challenger Integration Diagram
The following diagram reproduces the detailed inner structure of saigen and shows how a testcase can utilize the generator as imported Python modules to turbo-charge test-cases.

![confgen-saichallenger.svg](confgen-saichallenger.svg)
# TODO
* Reconcile the param dicts vs. param attributes obtained via Munch, use of scalar variables inside performance-heavy loops etc. There is a tradeoff between elegance, expressiveness and performance.
# IDEAS/Wish-List
* Expose yaml format, need to work on streaming output (bulk output was owrking but slow).
* Use logger instead of print to stderr
* logging levels -v, -vv, -vvv etc., otherwise silent on stderr
* -O, --optimize flags for speed or memory (for speed - expand lists in-memory and use orjson serializer, like original code)
* Use nested generators inside each sub-generator, instead of nested loops, to reduce in-memory usage; may require enhancing JSON output streaming to use recursion etc.
## Sample Config Format

This is taken from [sample_generator_output.txt](https://github.com/plvisiondevs/SAI-Challenger.OCP/pull/3/files#diff-76e960deeab1d16712519482c671943fb847332eca3d3ebd2152aaa96a3c120b) and is a temporary snapshot of work-in-progress; a final version will be provided in the future.

Compare this to the PTF test-case [test_saithrift_vnet.py](https://github.com/Azure/DASH/blob/main/dash-pipeline/tests/saithrift/ptf/vnet/test_saithrift_vnet.py) which contains a mix of saithrift-specific data structure creationg and API calls.


```
{
    "op" : "create",
    "type" : "OBJECT_TYPE_VIP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vip" : "192.168.0.1"
    },
    "attributes" : [ "SAI_VIP_ENTRY_ATTR_ACTION", "SAI_VIP_ENTRY_ACTION_ACCEPT" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_DIRECTION_LOOKUP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vni" : "2000"
    },
    "attributes" : [ "SAI_DIRECTION_LOOKUP_ENTRY_ATTR_ACTION", "SAI_DIRECTION_LOOKUP_ENTRY_ACTION_SET_OUTBOUND_DIRECTION" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
    "key": "$acl_in_1",
    "attributes" : [ "SAI_DASH_ACL_GROUP_ATTR_IP_ADDR_FAMILY", "SAI_IP_ADDR_FAMILY_IPV4" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
    "key": "$acl_out_1",
    "attributes" : [ "SAI_DASH_ACL_GROUP_ATTR_IP_ADDR_FAMILY", "SAI_IP_ADDR_FAMILY_IPV4" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_VNET",
    "key" : "$vnet_1",
    "attributes" : [ "SAI_VNET_ATTR_VNI", "2000" ]
},
{
    "op": "create",
    "type" : "SAI_OBJECT_TYPE_ENI",
    "key" : "$eni_id",
    "attributes" : [ "SAI_ENI_ATTR_CPS", "10000",
                     "SAI_ENI_ATTR_PPS", "100000",
                     "SAI_ENI_ATTR_FLOWS", "100000",
                     "SAI_ENI_ATTR_ADMIN_STATE", "True",
                     "SAI_ENI_ATTR_VM_UNDERLAY_DIP", "10.10.10.10",
                     "SAI_ENI_ATTR_VM_VNI", "9",
                     "SAI_ENI_ATTR_VNET_ID", "$vnet_1",
                     "SAI_ENI_ATTR_INBOUND_V4_STAGE1_DASH_ACL_GROUP_ID", "$acl_in_1",
                     "SAI_ENI_ATTR_INBOUND_V4_STAGE2_DASH_ACL_GROUP_ID", "$acl_in_1",
                     "SAI_ENI_ATTR_INBOUND_V4_STAGE3_DASH_ACL_GROUP_ID", "$acl_in_1",
                     "SAI_ENI_ATTR_INBOUND_V4_STAGE4_DASH_ACL_GROUP_ID", "$acl_in_1",
                     "SAI_ENI_ATTR_INBOUND_V4_STAGE5_DASH_ACL_GROUP_ID", "$acl_in_1",
                     "SAI_ENI_ATTR_INBOUND_V6_STAGE1_DASH_ACL_GROUP_ID", "$acl_out_1",
                     "SAI_ENI_ATTR_INBOUND_V6_STAGE2_DASH_ACL_GROUP_ID", "$acl_out_1",
                     "SAI_ENI_ATTR_INBOUND_V6_STAGE3_DASH_ACL_GROUP_ID", "$acl_out_1",
                     "SAI_ENI_ATTR_INBOUND_V6_STAGE4_DASH_ACL_GROUP_ID", "$acl_out_1",
                     "SAI_ENI_ATTR_INBOUND_V6_STAGE5_DASH_ACL_GROUP_ID", "$acl_out_1",
                     "SAI_ENI_ATTR_OUTBOUND_V4_STAGE1_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V4_STAGE2_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V4_STAGE3_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V4_STAGE4_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V4_STAGE5_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V6_STAGE1_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V6_STAGE2_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V6_STAGE3_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V6_STAGE4_DASH_ACL_GROUP_ID", "0",
                     "SAI_ENI_ATTR_OUTBOUND_V6_STAGE5_DASH_ACL_GROUP_ID", "0" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_ENI_ETHER_ADDRESS_MAP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "address" : "00:AA:AA:AA:AA:00"
    },
    "attributes" : [ "SAI_ENI_ETHER_ADDRESS_MAP_ENTRY_ATTR_ENI_ID", "$eni_id" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vni" : "1000",
    },
    "attributes" : [ "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION", "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_PA_VALIDATE" ]
},
{
    "op" : "create",
    "type" : "SAI_OBJECT_TYPE_PA_VALIDATION_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "eni_id" : "$eni_id",
        "sip" : "20.20.20.20",
        "vni" : "1000"
    },
    "attributes" : [ "SAI_PA_VALIDATION_ENTRY_ATTR_ACTION", "SAI_PA_VALIDATION_ENTRY_ACTION_PERMIT" ]
}



{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_PA_VALIDATION_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "eni_id" : "$eni_id",
        "sip" : "20.20.20.20",
        "vni" : "1000"
    }
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vni" : "1000",
    }
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_ENI_ETHER_ADDRESS_MAP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "address" : "00:AA:AA:AA:AA:00"
    }
},
{
    "op": "remove",
    "type" : "SAI_OBJECT_TYPE_ENI",
    "key" : "$eni_id"
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_VNET",
    "key" : "$vnet_1"
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
    "key": "$acl_out_1"
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
    "key": "$acl_in_1"
},
{
    "op" : "remove",
    "type" : "SAI_OBJECT_TYPE_DIRECTION_LOOKUP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vni" : "2000"
    }
},
{
    "op" : "remove",
    "type" : "OBJECT_TYPE_VIP_ENTRY",
    "key" : {
        "switch_id" : "$SWITCH_ID",
        "vip" : "192.168.0.1"
    }
}
```
## Comparisons - confgen, confgen2

### confgen - original design
Note I added some memory usage logging
```
chris@chris-z4:~/chris-DASH/DASH/test/confgen$ time ./generate.d.py 
Start: Memory: 11.7 MB, 
generating config
    enis.py
enis.generate() done: Memory: 11.7 MB, 
    aclgroups.py
aclgroups.generate() done: Memory: 1065.6 MB, 
    vpc.py
vpc.generate() done: Memory: 1065.6 MB, 
    vpcmappingtypes.py
vpcmappingtypes.generate() done: Memory: 1065.6 MB, 
    vpcmappings.py
vpcmappings.generate() done: Memory: 1997.9 MB, 
    routingappliances.py
routingappliances.generate() done: Memory: 1997.9 MB, 
    routetables.py
routetables.generate() done: Memory: 2257.6 MB, 
    prefixtags.py
prefixtags.generate() done: Memory: 2257.6 MB, 
config.update( all ) done: Memory: 2257.6 MB, 
writing the config to file
File write done: Memory: 3567.9 MB, 
done

real	1m15.912s
user	1m14.006s
sys	0m1.904s
```
## confgen2
```
Start: Memory: 19.1 MB, 
Generators instantiated: Memory: 19.1 MB, 
writeDictFileIter enter: Memory: 19.1 MB, 
Writing the json config to tmp_hero.json...
  Generating enis...
    enis: yielded 8 items: Memory: 19.1 MB, 
    wrote dict item 'enis': Memory: 19.1 MB, 
  Generating acl-groups...
    acl-groups: yielded 48 items: Memory: 19.4 MB, 
    wrote dict item 'acl-groups': Memory: 19.4 MB, 
  Generating vpc...
    vpc: generated 16 items: Memory: 19.4 MB, 
    wrote dict item 'vpc': Memory: 19.4 MB, 
  Generating vpc-mappings-routing-types...
    vpc-mappings-routing-types: generated 3 items: Memory: 19.4 MB, 
    wrote dict item 'vpc-mappings-routing-types': Memory: 19.4 MB, 
  Generating vpc-mappings...
    vpc-mappings: yielded 16 items: Memory: 19.4 MB, 
    wrote dict item 'vpc-mappings': Memory: 19.4 MB, 
  Generating routing-appliances...
    routing-appliances: yielded 16 items: Memory: 19.4 MB, 
    wrote dict item 'routing-appliances': Memory: 19.4 MB, 
  Generating route-tables...
    route-tables: yielded 8 items: Memory: 19.4 MB, 
    wrote dict item 'route-tables': Memory: 19.4 MB, 
  Generating prefix-tags...
    prefix-tags: yielded 16 items: Memory: 19.4 MB, 
    wrote dict item 'prefix-tags': Memory: 19.4 MB, 
writeDictFileIter exit: Memory: 19.4 MB, 
Done: Memory: 19.4 MB, 

real	1m33.970s
user	1m32.159s
sys	0m1.344s
```
