#!/usr/bin/python3

from confbase import *
from confutils import *
from copy import deepcopy
import sys
class AclGroups(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('acl-groups', params, args)
        self.rules = self.AclRulesIpv4(self.params)
        self.subgens = [self.rules]
    class AclRulesIpv4(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('rules', params, args)
            if hasattr(self, 'args'):
                self.eni_index = self.args.eni_index
                self.table_index = self.args.table_index
            else:
                self.eni_index = 1
                self.table_index = 1
        
        def items(self, eni_ndx=None, table_ndx=None):
            # allow using param value from command-line, or override from called
            if eni_ndx:
                eni_index=eni_ndx # from caller
            else:
                eni_index = self.eni_index # from constructor w/ cmd-line args
                
            if table_ndx:
                table_index=table_ndx # from caller
            else:
                table_index = self.table_index # from constructor w/ cmd-line args

            p=self.params
            cp=self.cooked_params
            IP_STEP1=cp.IP_STEP1
            IP_STEP2=cp.IP_STEP2
            IP_STEP3=cp.IP_STEP3
            IP_STEP4=cp.IP_STEP4
            IP_STEPE=cp.IP_STEPE
            IP_R_START=cp.IP_R_START
            IP_L_START=cp.IP_L_START
            ACL_RULES_NSG=p.ACL_RULES_NSG
            IP_PER_ACL_RULE=p.IP_PER_ACL_RULE

            # TODO - optimize, pass form caller
            local_ip = IP_L_START + (eni_index - 1) * IP_STEP4
            l_ip_ac = deepcopy(str(local_ip)+"/32")

            for ip_index in range(1, (ACL_RULES_NSG+1), 2):
                # rule_id_a = table_id * 10 * ACL_RULES_NSG + ip_index
                remote_ip_a = IP_R_START + (eni_index - 1) * IP_STEP4 + (
                    table_index - 1) * 4 * IP_STEP3 + (ip_index - 1) * IP_STEP2

                ip_list_a = [str(remote_ip_a + expanded_index * IP_STEPE)+"/32" for expanded_index in range(0, IP_PER_ACL_RULE)]
                ip_list_a.append(l_ip_ac)

                rule_a = {
                    "priority": ip_index,
                    "action": "allow",
                    "terminating": False,
                    "src_addrs": ip_list_a[:],
                    "dst_addrs":  ip_list_a[:],
                }
                self.numYields+=1
                # yield deepcopy(rule_a)
                yield self.renderItem(rule_a) 

                # rule_id_d = rule_id_a + 1
                remote_ip_d = remote_ip_a + IP_STEP1

                ip_list_d = [str(remote_ip_d + expanded_index * IP_STEPE)+"/32" for expanded_index in range(0, IP_PER_ACL_RULE)]
                ip_list_d.append(l_ip_ac)

                rule_d = {
                    "priority": ip_index+1,
                    "action": "deny",
                    "terminating": True,
                    "src_addrs": ip_list_d[:],
                    "dst_addrs":  ip_list_d[:],
                }
                self.numYields+=1
                # yield deepcopy(rule_d)
                yield self.renderItem(rule_d) 

            # add as last rule in last table from ingress and egress an allow rule for all the ip's from egress and ingress
            # TODO parameterize num tables
            if ((table_index - 1) % 3) == 2:
                # rule_id_a = table_id * 10 *ACL_RULES_NSG + ip_index
                all_ipsA = IP_R_START + (eni_index - 1) * IP_STEP4 + (table_index % 6) * 4 * IP_STEP3
                all_ipsB = all_ipsA + 1 * 4 * IP_STEP3
                all_ipsC = all_ipsA + 2 * 4 * IP_STEP3

                ip_list_all = [
                    l_ip_ac,
                    str(all_ipsA)+"/14",
                    str(all_ipsB)+"/14",
                    str(all_ipsC)+"/14",
                ]

                rule_allow_all = {
                    "priority": ip_index+2,
                    "action": "allow",
                    "terminating": "true",
                    "src_addrs": ip_list_all[:],
                    "dst_addrs":  ip_list_all[:],
                }
                self.numYields+=1
                # yield deepcopy(rule_allow_all)
                yield self.renderItem(rule_allow_all) 
   
    def items(self):
        self.log_verbose('  Generating %s...' % self.dictName())
        p=self.params
        cp=self.cooked_params
        IP_STEP4=cp.IP_STEP4
        IP_L_START=cp.IP_L_START
        ACL_TABLE_COUNT=p.ACL_TABLE_COUNT

        for eni_index in range(1, p.ENI_COUNT + 1):
            local_ip = IP_L_START + (eni_index - 1) * IP_STEP4
            l_ip_ac = deepcopy(str(local_ip)+"/32")

            for table_index in range(1, (ACL_TABLE_COUNT*2+1)):
                table_id = eni_index * 1000 + table_index
                acl_group = {
                        "ACL-GROUP:ENI:%d:TABLE:%d" % (eni_index, table_id): {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "ip_version": "IPv4",
                            self.rules.dictName(): (x for x in self.rules.items(eni_index, table_index)),
                            
                        }
                    }
                
                self.numYields+=1
                yield self.renderItem(acl_group)
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.rules.dictName(), self.rules.itemsGenerated()))


    def main(self):
        program = sys.argv[0].replace('./.','.')
        parser=commonArgParser()

        parser.add_argument('-a', '--acls-ipv4', action='store_true',
                help='Generate IPv4 ACL group tables, suppress top-level container')

        parser.add_argument('-e', '--eni-index', type=int, default=1,
                help='Specify single ENI index (use with -a option only)')

        parser.add_argument('-t', '--table-index', type=int, default=1,
                help='Specify single table index (use with -a option only)')

        parser.epilog = textwrap.dedent(common_arg_epilog + '''

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
        '''.replace('dashgen/enis.py',program).replace('./.','.'))

        common_parse_args(self, parser)         
        self.log_mem("Start")
        suppress_top_level = False

        if self.args.acls_ipv4:
            acl_in=self.AclRulesIpv4(args=self.args)
            common_output(acl_in)
            suppress_top_level = True

        if not suppress_top_level:
            common_output(self)

        self.log_mem("Done")

if __name__ == "__main__":
    conf=AclGroups()
    conf.main()
