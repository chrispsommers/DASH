#!/usr/bin/python3

from confbase import *
from confutils import *
import sys
class PrefixTags(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('prefix-tags', params, args)

    def items(self):
        self.numYields = 0
        self.log_verbose('  Generating %s...' % self.dictName())
        p=self.params
        cp=self.cooked_params
        for eni_index in range(1, p.ENI_COUNT+1):
            IP_L = cp.IP_L_START + (eni_index - 1) * cp.IP_STEP4
            r_vpc = eni_index + p.ENI_L2R_STEP
            IP_R = cp.IP_R_START + (eni_index - 1) * cp.IP_STEP4
            self.numYields+=1
            yield \
                {
                    "PREFIX-TAG:VPC:%d" % eni_index: {
                        "prefix-tag-id": "%d" % eni_index,
                        "prefix-tag-number": eni_index,
                        "ip-prefixes-ipv4": [
                            "%s/32" % IP_L
                        ]
                    },
                }

            self.numYields+=1
            yield \
                {
                    "PREFIX-TAG:VPC:%d" % r_vpc: {
                        "prefix-tag-id": "%d" % r_vpc,
                        "prefix-tag-number": r_vpc,
                        "ip-prefixes-ipv4": [
                            "%s/9" % IP_R
                        ]
                    },
                }
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.numYields))
            
if __name__ == "__main__":
    conf=PrefixTags()
    common_main(conf)
