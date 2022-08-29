#!/usr/bin/python3

from confbase import *
from confutils import *
import sys
class Enis(ConfBase):

    def __init__(self, params={}, args=None):
        super().__init__('enis', params, args)
        self.acl_in = self.AclsV4In(self.params)
        self.acl_out = self.AclsV4Out(self.params)
        self.subgens = [self.acl_in, self.acl_out]

    class AclsV4In(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('acls-v4-in', params, args)
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
            for table_index in range(1, (p.ACL_TABLE_COUNT*2+1)):
                table_id = eni_index * 1000 + table_index

                stage = (table_index - 1) % 3 + 1
                if table_index < 4:
                    self.numYields+=1
                    yield self.renderItem( \
                        {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "stage": stage
                        })
                    
                else:
                    continue


    class AclsV4Out(ConfBase):
        def __init__(self, params={}, args=None):
            super().__init__('acls-v4-out', params, args)
            if hasattr(self, 'args'):
                # extract params from cmd-line
                self.eni_index = self.args.eni_index
            else:
                # default value
                self.eni_index = 1

        def items(self, eni=None):
            # allow using param value from command-line, or override from called
            if eni:
                eni_index=eni # from caller
            else:
                eni_index = self.eni_index # from constructor w/ cmd-line args
            p=self.params
            for table_index in range(1, (p.ACL_TABLE_COUNT*2+1)):
                table_id = eni_index * 1000 + table_index

                stage = (table_index - 1) % 3 + 1

                if table_index < 4:
                    continue
                    
                else:
                    self.numYields+=1
                    yield self.renderItem( \
                        {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "stage": stage
                        })


    def items(self):
        self.numYields = 0
        log_msg('  Generating %s...' % self.dictName(), self.args.verbose)
        p=self.params
        cp=self.cooked_params

        for eni_index in range(1, p.ENI_COUNT+1):
            local_mac = str(macaddress.MAC(int(cp.MAC_L_START)+(eni_index - 1)*int(macaddress.MAC(p.ENI_MAC_STEP)))).replace('-', ':')

            self.numYields+=1
            yield self.renderItem( \
                {
                    'ENI:%d' % eni_index: {
                        'eni-id': 'eni-%d' % eni_index,
                        'mac': local_mac,
                        'vpcs': [
                            eni_index
                        ],
                        self.acl_in.dictName(): (x for x in self.acl_in.items(eni_index)),
                        self.acl_out.dictName(): (x for x in self.acl_out.items(eni_index)),
                        "route-table-v4": "route-table-%d" % eni_index
                    },
                })
        self.log_mem('    Finished generating %s' % self.dictName())
        self.log_details('    %s: yielded %d items' % (self.dictName(), self.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.acl_in.dictName(), self.acl_in.itemsGenerated()))
        self.log_details('    %s: yielded %d items' % (self.acl_out.dictName(), self.acl_out.itemsGenerated()))

    def main(self):
        program = sys.argv[0].replace('./.','.')
        parser=commonArgParser()

        parser.add_argument('-a', '--acls-in', action='store_true',
                help='Generate ACL IN tables (single ENI), suppress top-level container')

        parser.add_argument('-A', '--acls-out', action='store_true',
                help='Generate ACL OUT tables (single ENI), suppress top-level container')

        parser.add_argument('-e', '--eni-index', type=int, default=1,
                help='Specify single ENI index (use with -aA options only)')

        parser.epilog = textwrap.dedent(common_arg_epilog + '''

ENI-specific Examples:
======================
These options allow you to run a specific sub-generator with narrow parameters for ENI.
Use -a, -A to generate ACL in and/or out tables for a single ENI.
Omit -a, -A to generate entire ACL group config per input PARAMs.
Use repeatedly if you need more ENIs, or write a custom program for other options.

./dashgen/enis.py -a -e 3                               - generate acl-in entries only, for ENI index 3
./dashgen/enis.py -aA -e 3                              - generate acl-in and acl-out entries, for ENI index 3
        '''.replace('dashgen/enis.py',program).replace('./.','.'))

        common_parse_args(self, parser)         
        self.log_mem("Start")
        suppress_top_level = False

        if self.args.acls_in:
            acl_in=self.AclsV4In(args=self.args)
            common_output(acl_in)
            suppress_top_level = True

        if self.args.acls_out:
            acl_out=self.AclsV4Out(args=self.args)
            common_output(acl_out)
            suppress_top_level = True
            
        if not suppress_top_level:
            common_output(self)

        self.log_mem("Done")

if __name__ == "__main__":

    conf=Enis()
    conf.main()
