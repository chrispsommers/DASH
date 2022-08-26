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
            IP_STEP1=cp.IP_STEP1
            IP_STEP4=cp.IP_STEP4
            IP_L_START=cp.IP_L_START
            IP_ROUTE_DIVIDER_PER_ACL_RULE=p.IP_ROUTE_DIVIDER_PER_ACL_RULE
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
        log_msg('  Generating %s...' % self.dictName(), self.args.verbose)
        p=self.params
        cp=self.cooked_params
        # optimizations:
        IP_ROUTE_DIVIDER_PER_ACL_RULE=p.IP_ROUTE_DIVIDER_PER_ACL_RULE
        # IP_PER_ACL_RULE=p.IP_PER_ACL_RULE
        IP_STEP1=cp.IP_STEP1
        # IP_STEP2=cp.IP_STEP2
        # IP_STEP3=cp.IP_STEP3
        # IP_STEP4=cp.IP_STEP4
        # IP_STEP1_MULT=IP_ROUTE_DIVIDER_PER_ACL_RULE * IP_STEP1
        # IP_R_START=cp.IP_R_START
        # IP_L_START=cp.IP_L_START
        # ACL_TABLE_COUNT=p.ACL_TABLE_COUNT
        # ACL_RULES_NSG=p.ACL_RULES_NSG
        # ENI_L2R_STEP=p.ENI_L2R_STEP

        # nr_of_routes_prefixes = int(math.log(p.IP_ROUTE_DIVIDER_PER_ACL_RULE, 2))
        
        for eni_index in range(1, p.ENI_COUNT+1):
            # routes = []
            # ip_prefixes = []
            # ip_prefixes_append = ip_prefixes.append

            # IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            # r_vpc = eni_index + ENI_L2R_STEP
            # # IP_R = IP_R_START + (eni_index - 1) * IP_STEP4
            # routes.append(
            #     {
            #         "ip-prefixes": ["%s/32" % IP_L],
            #         "action": {
            #             "routing-type": "vpc",
            #             "vpc-id": "vpc-%d" % eni_index
            #         }
            #     }
            # )

            # for table_index in range(1, (ACL_TABLE_COUNT*2+1)):
            #     #table_id = eni_index * 1000 + table_index

            #     for acl_index in range(1, (ACL_RULES_NSG+1)):
            #         remote_ip = IP_R_START + (eni_index - 1) * IP_STEP4 + (table_index - 1) * 4 * IP_STEP3 + (acl_index - 1) * IP_STEP2
            #         no_of_route_groups = IP_PER_ACL_RULE // IP_ROUTE_DIVIDER_PER_ACL_RULE
            #         for ip_index in range(0, no_of_route_groups):
            #             ip_prefix = remote_ip - 1 + ip_index * IP_STEP1_MULT
            #             for prefix_index in range(nr_of_routes_prefixes, 0, -1):
            #                 # nr_of_ips = int(math.pow(2, prefix_index-1))
            #                 nr_of_ips = 1<< (prefix_index-1)
            #                 mask = 32 - prefix_index + 1
            #                 if mask == 32:
            #                     ip_prefix = ip_prefix + 1
            #                 ip_prefixes_append("%s/%d" % (ip_prefix, mask))
            #                 ip_prefix = ip_prefix + IP_STEP1 * nr_of_ips

            # routes.append(
            #     {
            #         "ip-prefixes": ip_prefixes,
            #         "action": {
            #             "routing-type": "vpc",
            #             "vpc-id": "vpc-%d" % r_vpc
            #         }
            #     }
            # )

            self.numYields+=1
            yield \
                {
                    "ROUTE-TABLE:%d" % eni_index: {
                        "route-table-id": "route-table-%d" % eni_index,
                        "ip-version": "IPv4",
                        # "routes": routes
                        self.routes.dictName(): (x for x in self.routes.items(eni_index)),
                    }
                }
        log_memory('    Finished generating %s' % self.dictName(), self.args.detailed_stats)
        log_msg('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()), self.args.detailed_stats)
        log_msg('    %s: yielded %d items' % (self.routes.dictName(), self.routes.itemsGenerated()), self.args.detailed_stats)
        log_msg('    %s: yielded %d items' % (self.routes.ip_prefixes.dictName(), self.routes.ip_prefixes.itemsGenerated()), self.args.detailed_stats)

if __name__ == "__main__":
    conf=RouteTables()
    common_main(conf)