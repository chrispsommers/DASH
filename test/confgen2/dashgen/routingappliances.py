#!/usr/bin/python3

from variables import *
from confbase import *
from confutils import *
from copy import deepcopy
import sys
class RoutingAppliances(ConfBase):

    def __init__(self, params={}):
        super().__init__('routing-appliances', params)
    
    def items(self):
        self.numYields = 0
        print('  Generating %s...' % self.dictname, file=sys.stderr)
        p=self.params

        for eni_index in range(1, p.ENI_COUNT+1):
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
        log_memory('    %s: yielded %d items' % (self.dictname, self.numYields))

if __name__ == "__main__":
    conf=RoutingAppliances()
    common_main(conf)