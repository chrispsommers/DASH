#!/usr/bin/python3

import io, sys
# import orjson
# import yaml
import dashgen
import argparse
from dashgen.confbase import *
from dashgen.confutils import *

parser = commonArgParser()
args = parser.parse_args()

class DashConfig(ConfBase):

        def __init__(self, params={}, args=None):
                super().__init__('dash-config', params, args)

        def generate(self):
                # Pass top-level params to sub-generators.
                # Future - can pass some overridden values if needed.
                enis = dashgen.enis.Enis(self.params_dict, self.args)
                aclgroups = dashgen.aclgroups.AclGroups(self.params_dict, args)
                vpcs = dashgen.vpcs.Vpcs(self.params_dict, args)
                vpcmappingtypes = dashgen.vpcmappingtypes.VpcMappingTypes(self.params_dict, args)
                vpcmappings = dashgen.vpcmappings.VpcMappings(self.params_dict, args)
                routingappliances = dashgen.routingappliances.RoutingAppliances(self.params_dict, args)
                routetables = dashgen.routetables.RouteTables(self.params_dict, args)
                prefixtags = dashgen.prefixtags.PrefixTags(self.params_dict, args)

                self.subgens = [
                        enis,
                        aclgroups,
                        vpcs,
                        vpcmappingtypes,
                        vpcmappings,
                        routingappliances,
                        routetables,
                        prefixtags
                ]
                log_memory("Generators instantiated", self.args.detailed_stats)

                # This instantiates config in-memory - could use if want to output with orjson for speed
                # def toDict(self):
                #         c = {}
                #         for i in self.subgens:
                #                 c.update(i.toDict()) 
                #         log_memory("toDict()")
                #         return c

        def itemsGenerated(self):
                """ we don't count yields, we count # subgens"""
                return len(self.subgens)

        def toDict(self):
                """Expensive - runs all generators"""
                return {x.dictName():x.items() for x in self.subgens}

        def items(self):
                """Expensive - runs all generators"""
                return (c.items() for c in self.subgens)

        def __str__(self):
                """String repr of all items in generator"""
                if len(self.subgens) > 0:
                        subtotal = sum(c.itemsGenerated() for c in self.subgens)

                        return '%s: %d items, %d sub-items:\n' % \
                                (self.dictName(), self.itemsGenerated(), self.subItemsGenerated()) + \
                                '  ' + \
                                '\n  '.join(c.__str__() for c in self.subgens)
                else:
                        return '%s: %d items' % (self.dictName(), self.itemsGenerated())


if __name__ == "__main__":
    conf=DashConfig()
    common_parse_args(conf)

    log_memory("Start", conf.args.detailed_stats)
    conf.generate()
    common_output(conf)
    log_memory("Done", conf.args.detailed_stats)
