#!/usr/bin/python3

from confbase import *
from confutils import *
import sys
class VpcMappingTypes(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('vpc-mappings-routing-types', params, args)
    
    def items(self):
        log_msg('  Generating %s...' % self.dictName(), self.args.verbose)
        p=self.params
        cp=self.cooked_params

        vpcmappingtypes = [
            "vpc",
            "privatelink",
            "privatelinknsg"
        ]

        # return generator from list for consistency with other subgenerators
        for x in vpcmappingtypes:

            self.numYields+=1
            yield x
        log_memory('    Finished generating %s' % self.dictName(), self.args.detailed_stats)
        log_msg('    %s: yielded %d items' % (self.dictName(), self.numYields), self.args.detailed_stats)

if __name__ == "__main__":
    conf=VpcMappingTypes()
    common_main(conf)