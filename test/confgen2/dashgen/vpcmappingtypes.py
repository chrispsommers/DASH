#!/usr/bin/python3

from confbase import *
from confutils import *
import sys
class VpcMappingTypes(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('vpc-mappings-routing-types', params, args)
    
    def items(self):
        self.log_verbose('  Generating %s...' % self.dictName())

        vpcmappingtypes = [
            "vpc",
            "privatelink",
            "privatelinknsg"
        ]

        # return generator from list for consistency with other subgenerators
        for x in vpcmappingtypes:

            self.numYields+=1
            yield x
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.numYields))

if __name__ == "__main__":
    conf=VpcMappingTypes()
    common_main(conf)