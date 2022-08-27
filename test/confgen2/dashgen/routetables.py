#!/usr/bin/python3

from confbase import *
from confutils import *
# from copy import deepcopy
import sys
import math

class RouteTables(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('route-tables', params, args)
        self.routes = self.Routes(self.params)
        self.subgens = [self.routes]

    class IpPrefixes(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('ip-prefixes', params, args)
            if hasattr(self, 'args'):
                self.eni_index = self.args.eni_index
            else:
                self.eni_index = 1

        def items(self, eni=None):
            # allow using param value from command-line, or override from called
            if eni:
                eni_index=eni
            else:
                eni_index = self.eni_index

            p=self.params
            cp=self.cooked_params
            IP_STEP1=cp.IP_STEP1
            IP_STEP2=cp.IP_STEP2
            IP_STEP3=cp.IP_STEP3
            IP_STEP4=cp.IP_STEP4
            IP_R_START=cp.IP_R_START
            IP_ROUTE_DIVIDER_PER_ACL_RULE=p.IP_ROUTE_DIVIDER_PER_ACL_RULE
            ACL_TABLE_COUNT=p.ACL_TABLE_COUNT
            ACL_RULES_NSG=p.ACL_RULES_NSG
            IP_STEP1_MULT=IP_ROUTE_DIVIDER_PER_ACL_RULE * IP_STEP1

            nr_of_routes_prefixes = int(math.log(IP_ROUTE_DIVIDER_PER_ACL_RULE, 2))
            no_of_route_groups = p.IP_PER_ACL_RULE // IP_ROUTE_DIVIDER_PER_ACL_RULE


            for table_index in range(1, (ACL_TABLE_COUNT*2+1)):
                #table_id = eni_index * 1000 + table_index

                for acl_index in range(1, (ACL_RULES_NSG+1)):
                    remote_ip = IP_R_START + (eni_index - 1) * IP_STEP4 + (table_index - 1) * 4 * IP_STEP3 + (acl_index - 1) * IP_STEP2
                    for ip_index in range(0, no_of_route_groups):
                        ip_prefix = remote_ip - 1 + ip_index * IP_STEP1_MULT
                        for prefix_index in range(nr_of_routes_prefixes, 0, -1):
                            # nr_of_ips = int(math.pow(2, prefix_index-1))
                            nr_of_ips = 1<< (prefix_index-1)
                            mask = 32 - prefix_index + 1
                            if mask == 32:
                                ip_prefix = ip_prefix + 1
                            self.numYields+=1
                            yield "%s/%d" % (ip_prefix, mask)
                            ip_prefix = ip_prefix + IP_STEP1 * nr_of_ips


    class Routes(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('routes', params, args)
            self.ip_prefixes = RouteTables.IpPrefixes(self.params)
            self.subgens = [self.ip_prefixes]
            if hasattr(self, 'args'):
                self.eni_index = self.args.eni_index
            else:
                self.eni_index = 1

        def items(self, eni=None):
            # allow using param value from command-line, or override from called
            if eni:
                eni_index=eni
            else:
                eni_index = self.eni_index
                
            p=self.params
            cp=self.cooked_params
            IP_STEP4=cp.IP_STEP4
            IP_L_START=cp.IP_L_START
            ENI_L2R_STEP=p.ENI_L2R_STEP

            IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            r_vpc = eni_index + ENI_L2R_STEP

            self.numYields+=1
            yield \
                {
                    "ip-prefixes": ["%s/32" % IP_L],
                    "action": {
                        "routing-type": "vpc",
                        "vpc-id": "vpc-%d" % eni_index
                    }
                }

            self.numYields+=1
            yield \
                {
                    self.ip_prefixes.dictName(): (x for x in self.ip_prefixes.items(eni_index)),
                    "action": {
                        "routing-type": "vpc",
                        "vpc-id": "vpc-%d" % r_vpc
                    }
                }

    def items(self):
        self.numYields = 0
        self.log_verbose('  Generating %s...' % self.dictName())
        p=self.params
        cp=self.cooked_params
        for eni_index in range(1, p.ENI_COUNT+1):

            self.numYields+=1
            yield \
                {
                    "ROUTE-TABLE:%d" % eni_index: {
                        "route-table-id": "route-table-%d" % eni_index,
                        "ip-version": "IPv4",
                        self.routes.dictName(): (x for x in self.routes.items(eni_index)),
                    }
                }
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.routes.dictName(), self.routes.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.routes.ip_prefixes.dictName(), self.routes.ip_prefixes.itemsGenerated()))

if __name__ == "__main__":
    conf=RouteTables()
    parser=commonArgParser()

    parser.add_argument('-i', '--ip-prefixes', action='store_true',
            help='Generate ip-prefixes, suppress top-level container')

    parser.add_argument('-r', '--routes', action='store_true',
            help='Generate routes, suppress top-level container')

    parser.add_argument('-e', '--eni-index', type=int, default=1,
            help='Specify single ENI index (use with -ir options only)')

    parser.epilog = textwrap.dedent(common_arg_epilog + '''

Routetables-specific Examples:
============================

The -i option allows you to generate ip-prefixes only for one ENI.
The -r option allows you to generate routes only for one ENI.
Use repeatedly if you need more instances, or write a custom program for other options.
Omit -ir to generate entire route tables config per input PARAMs.

python3 dashgen/routetables.py [-p PARAM_FILE] [-P PARAMS]       - generate route tables from global options
python3 dashgen/routetables.py -i                                - generate ip_prefixes only for ENI=1
python3 dashgen/routetables.py -r -e 3                           - generate routes only for ENI=3
    ''')

    common_parse_args(conf, parser)         
    conf.log_mem("Start")
    suppress_top_level = False

    if conf.args.ip_prefixes:
        ip_pre=conf.IpPrefixes(args=conf.args)
        common_output(ip_pre)
        suppress_top_level = True

    if conf.args.routes:
        routes=conf.Routes(args=conf.args)
        common_output(routes)
        suppress_top_level = True

    if not suppress_top_level:
        common_output(conf)

