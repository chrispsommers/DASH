#!/usr/bin/python3

from confbase import *
from confutils import *
class VpcMappings(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('vpc-mappings', params, args)
        self.l_mappings = self.LocalVpcMappings(self.params)
        self.r_mappings = self.RemoteVpcMappings(self.params)
        self.subgens = [self.l_mappings, self.r_mappings]

    class LocalVpcMappings(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('mappings', params, args)
            if hasattr(self, 'args'):
                self.eni_index = self.args.eni_index
            else:
                self.eni_index = 1

        def items(self, eni_ndx=None):
            # allow using param value from command-line, or override from called
            if eni_ndx:
                eni_index=eni_ndx # from caller
            else:
                eni_index = self.eni_index # from constructor w/ cmd-line args

            p=self.params
            cp=self.cooked_params
            IP_STEP1=cp.IP_STEP1
            IP_STEP4=cp.IP_STEP4
            IP_L_START=cp.IP_L_START
            ENI_MAC_STEP=p.ENI_MAC_STEP
            MAC_L_START=cp.MAC_L_START
            PAL = cp.PAL
            pal = PAL + eni_index*IP_STEP1
            local_ip = IP_L_START + (eni_index - 1) * IP_STEP4
            local_mac = str(
                macaddress.MAC(
                    int(MAC_L_START) +
                    (eni_index - 1) * int(macaddress.MAC(ENI_MAC_STEP))
                )
            ).replace('-', ':')

            self.numYields+=1
            yield \
                {
                    "routing-type": "vpc-direct",
                    "overlay-ip-address": "%s" % local_ip,
                    "underlay-ip-address": "%s" % pal,
                    "mac": local_mac
                }

    class RemoteVpcMappings(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('mappings', params, args)
            if hasattr(self, 'args'):
                self.eni_index = self.args.eni_index
                self.table_index = self.args.table_index
            else:
                self.eni_index = 1
                self.table_index = 1

        def items(self, eni_ndx=None):
            # allow using param value from command-line, or override from called
            if eni_ndx:
                eni_index=eni_ndx # from caller
            else:
                eni_index = self.eni_index # from constructor w/ cmd-line args
            p=self.params
            cp=self.cooked_params
            PAR = cp.PAR
            IP_STEP1=cp.IP_STEP1
            IP_STEP2=cp.IP_STEP2
            IP_STEP3=cp.IP_STEP3
            IP_STEP4=cp.IP_STEP4
            IP_R_START=cp.IP_R_START
            ACL_TABLE_COUNT=p.ACL_TABLE_COUNT
            ACL_RULES_NSG=p.ACL_RULES_NSG
            ENI_MAC_STEP=p.ENI_MAC_STEP
            ACL_TABLE_MAC_STEP=p.ACL_TABLE_MAC_STEP
            ACL_POLICY_MAC_STEP=p.ACL_POLICY_MAC_STEP
            IP_MAPPED_PER_ACL_RULE=p.IP_MAPPED_PER_ACL_RULE

            par = PAR + eni_index*IP_STEP1
            for table_index in range(1, (ACL_TABLE_COUNT*2+1)):
                for ip_index in range(1, (ACL_RULES_NSG+1)):
                    remote_ip = IP_R_START + (eni_index - 1) * IP_STEP4 + (table_index - 1) * 4 * IP_STEP3 + (ip_index - 1) * IP_STEP2
                    remote_mac = str(
                        macaddress.MAC(
                            int(macaddress.MAC('00:1B:6E:80:00:01')) +
                            (eni_index - 1) * int(macaddress.MAC(ENI_MAC_STEP)) +
                            (table_index - 1) * int(macaddress.MAC(ACL_TABLE_MAC_STEP)) +
                            (ip_index - 1) * int(macaddress.MAC(ACL_POLICY_MAC_STEP))
                        )
                    ).replace('-', ':')

                    for i in range(IP_MAPPED_PER_ACL_RULE):
                        remote_expanded_ip = remote_ip + i
                        remote_expanded_mac = str(
                            macaddress.MAC(
                                int(macaddress.MAC(remote_mac)) + i
                            )
                        ).replace('-', ':')
                        
                        self.numYields+=1
                        yield \
                            {
                                "routing-type": "vpc-direct",
                                "overlay-ip-address": "%s" % remote_expanded_ip,
                                "underlay-ip-address": "%s" % par,
                                "mac": remote_expanded_mac
                            }
    
    def items(self):
        self.log_verbose('  Generating %s...' % self.dictName())
        p=self.params
        cp=self.cooked_params
        PAL = cp.PAL
        IP_STEP1=cp.IP_STEP1
        IP_STEP4=cp.IP_STEP4
        IP_L_START=cp.IP_L_START
        ENI_MAC_STEP=p.ENI_MAC_STEP
        MAC_L_START=cp.MAC_L_START
        ENI_COUNT=p.ENI_COUNT

        for eni_index in range(1, ENI_COUNT + 1):

            l_vpc_mapping = {
                    "MAPPINGS:VPC:%d" % eni_index: {
                        "vpc-id": "vpc-%d" % eni_index,
                        self.l_mappings.dictName():(x for x in self.l_mappings.items(eni_index))
                    }
                }

            self.numYields+=1
            yield l_vpc_mapping

            r_vpc = eni_index + p.ENI_L2R_STEP
            r_vpc_mapping = {
                    "MAPPINGS:VPC:%d" % r_vpc: {
                        "vpc-id": "vpc-%d" % r_vpc,
                        self.r_mappings.dictName(): (x for x in self.r_mappings.items(eni_index))
                    }
                }

            self.numYields+=1
            yield r_vpc_mapping
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.r_mappings.dictName(), self.r_mappings.itemsGenerated()))

if __name__ == "__main__":
    conf=VpcMappings()

    parser=commonArgParser()

    parser.add_argument('-i', '--ip-prefixes', action='store_true',
            help='Generate ip-prefixes, suppress top-level container')

    parser.add_argument('-l', '--local-mappings', action='store_true',
            help='Generate local mappings, suppress top-level container')

    parser.add_argument('-r', '--remote-mappings', action='store_true',
            help='Generate remote mappings, suppress top-level container')

    parser.add_argument('-e', '--eni-index', type=int, default=1,
            help='Specify single ENI index (use with -lr options only)')

    parser.add_argument('-t', '--table-index', type=int, default=1,
            help='Specify single table index (use with -lr options only)')

    parser.epilog = textwrap.dedent(common_arg_epilog + '''

VPC-Mappings-specific Examples:
============================

The -lr options allows you to generate local or remote VPC mappings only for one ENI without outer containers.
Use repeatedly if you need more instances, or write a custom program for other options.
Omit -lr to generate entire mapping tables config per input PARAMs.

python3 dashgen/vpcmappings.py [-p PARAM_FILE] [-P PARAMS]       - generate mappings from global options
python3 dashgen/vpcmappings.py -l                                - generate local mappings only for ENI=1
python3 dashgen/vpcmappings.py -r -e 3                           - generate remote mappings only for ENI=3
    ''')

    common_parse_args(conf, parser)         
    conf.log_mem("Start")
    suppress_top_level = False

    if conf.args.local_mappings:
        l_mappings=conf.LocalVpcMappings(args=conf.args)
        common_output(l_mappings)
        suppress_top_level = True

    if conf.args.remote_mappings:
        r_mappings=conf.RemoteVpcMappings(args=conf.args)
        common_output(r_mappings)
        suppress_top_level = True

    if not suppress_top_level:
        common_output(conf)

