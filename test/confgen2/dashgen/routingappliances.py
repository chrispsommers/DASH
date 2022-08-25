#!/usr/bin/python3

from confbase import *
from confutils import *
from copy import deepcopy
import sys
class RoutingAppliances(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('routing-appliances', params, args)
    
    def items(self):
        log_msg('  Generating %s...' % self.dictName(), self.args.verbose)
        p=self.params
        cp=self.cooked_params
        # optimizations:
        IP_STEP4=cp.IP_STEP4
        IP_R_START=cp.IP_R_START
        IP_L_START=cp.IP_L_START
        ENI_COUNT=p.ENI_COUNT
        ENI_L2R_STEP=p.ENI_L2R_STEP

        for eni_index in range(1, ENI_COUNT+1):
            IP_L = IP_L_START + (eni_index - 1) * IP_STEP4
            r_vpc = eni_index + ENI_L2R_STEP
            IP_R = IP_R_START + (eni_index - 1) * IP_STEP4
            self.numYields+=1
            yield \
                {
                    "ROUTING-APPLIANCE:%d" % eni_index: {
                        "appliance-id": "appliance-%d" % eni_index,
                        "routing-appliance-id": eni_index,
                        "routing-appliance-addresses": [
                            "%s/32" % IP_L
                        ],
                        "encap-type": "vxlan",
                        "vni-key": eni_index
                    }
                }
            
            self.numYields+=1
            yield \
                {
                    "ROUTING-APPLIANCE:%d" % r_vpc: {
                        "appliance-id": "appliance-%d" % r_vpc,
                        "routing-appliance-id": r_vpc,
                        "routing-appliance-addresses": [
                            "%s/9" % IP_R
                        ],
                        "encap-type": "vxlan",
                        "vni-key": r_vpc
                    },
                }
        log_memory('    Finished generating %s' % self.dictName(), self.args.detailed_stats)
        log_msg('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()), self.args.detailed_stats)

if __name__ == "__main__":
    conf=RoutingAppliances()
    common_main(conf)