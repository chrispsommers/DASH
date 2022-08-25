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
                # Pass top-level params to sub-generrators.
                # Future - can pass some overridden values if needed.
                enis = dashgen.enis.Enis(self.params_dict, self.args)
                aclgroups = dashgen.aclgroups.AclGroups(self.params_dict, args)
                vpcs = dashgen.vpcs.Vpcs(self.params_dict, args)
                vpcmappingtypes = dashgen.vpcmappingtypes.VpcMappingTypes(self.params_dict, args)
                vpcmappings = dashgen.vpcmappings.VpcMappings(self.params_dict, args)
                routingappliances = dashgen.routingappliances.RoutingAppliances(self.params_dict, args)
                routetables = dashgen.routetables.RouteTables(self.params_dict, args)
                prefixtags = dashgen.prefixtags.PrefixTags(self.params_dict, args)

                self.configs = [
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
                #         for i in self.configs:
                #                 c.update(i.toDict()) 
                #         log_memory("toDict()")
                #         return c

        def toDict(self):
                return {x.dictName():x.items() for x in self.configs}

        def items(self):
                """Expensive - runs all generators"""
                return (c.items() for c in self.configs)

        def __str__(self):
                """String repr of all items in generator"""
                return '%s: %d total items:\n' % (self.dictName(), sum(c.itemsGenerated() for c in self.configs)) + \
                        '  ' +\
                        '\n  '.join(c.__str__() for c in self.configs)


if __name__ == "__main__":
    conf=DashConfig()
    common_parse_args(conf)

    log_memory("Start", conf.args.detailed_stats)
    conf.generate()
    common_output(conf)
    if conf.args.summary_stats:
        print (conf.__str__(), file=sys.stderr)
    log_memory("Done", conf.args.detailed_stats)
