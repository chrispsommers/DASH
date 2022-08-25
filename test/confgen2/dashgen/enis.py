#!/usr/bin/python3

from confbase import *
from confutils import *
import sys
class Enis(ConfBase):

    def __init__(self, params={}):
        super().__init__('enis', params)
 
    class acls_v4_in(ConfBase):
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
                    yield \
                        {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "stage": stage
                        }
                    
                else:
                    continue

    class acls_v4_out(ConfBase):
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
                    yield \
                        {
                            "acl-group-id": "acl-group-%d" % table_id,
                            "stage": stage
                        }


    def items(self):
        self.numYields = 0
        print('  Generating %s...' % self.dictName(), file=sys.stderr)
        p=self.params
        cp=self.cooked_params
        acl_in = self.acls_v4_in(self.params)
        acl_out = self.acls_v4_out(self.params)

        for eni_index in range(1, p.ENI_COUNT+1):
            local_mac = str(macaddress.MAC(int(cp.MAC_L_START)+(eni_index - 1)*int(macaddress.MAC(p.ENI_MAC_STEP)))).replace('-', ':')

            # acls_v4_in = []
            # acls_v4_out = []

            # for table_index in range(1, (p.ACL_TABLE_COUNT*2+1)):
            #     table_id = eni_index * 1000 + table_index

            #     stage = (table_index - 1) % 3 + 1
            #     if table_index < 4:
            #         acls_v4_in.append(
            #             {
            #                 "acl-group-id": "acl-group-%d" % table_id,
            #                 "stage": stage
            #             }
            #         )
            #     else:
            #         acls_v4_out.append(
            #             {
            #                 "acl-group-id": "acl-group-%d" % table_id,
            #                 "stage": stage
            #             }
            #         )

            self.numYields+=1
            yield \
                {
                    'ENI:%d' % eni_index: {
                        'eni-id': 'eni-%d' % eni_index,
                        'mac': local_mac,
                        'vpcs': [
                            eni_index
                        ],
                        # "acls-v4-in": acls_v4_in,
                        # "acls-v4-out": acls_v4_out,
                        acl_in.dictName(): (x for x in acl_in.items(eni_index)),
                        acl_out.dictName(): (x for x in acl_out.items(eni_index)),
                        "route-table-v4": "route-table-%d" % eni_index
                    },
                }
        log_memory('    %s: yielded %d items' % (self.dictName(), self.numYields))

if __name__ == "__main__":
    conf=Enis()
    parser=commonArgParser()

    parser.add_argument('-a', '--acls-in', action='store_true',
            help='Generate ACL IN tables, supress top-level container')

    parser.add_argument('-A', '--acls-out', action='store_true',
            help='Generate ACL OUT tables, suppress top-level container')

    parser.add_argument('-i', '--eni-index', type=int, default=1,
            help='Generate ACL OUT tables, suppress top-level container')

    parser.epilog = textwrap.dedent(common_arg_epilog + '''

ENI-specific Examples:
======================
python3 dashgen/enis.py -a -i 3                               - generate acl-in entries only, for ENI index 3
python3 dashgen/enis.py -aA -i 3                              - generate acl-in and acl-out entries, for ENI index 3
    ''')

    common_parse_args(conf, parser)         
    log_memory("Start")
    suppress_top_level = False

    if conf.args.acls_in:
        acl_in=conf.acls_v4_in(args=conf.args)
        common_output(acl_in)
        suppress_top_level = True

    if conf.args.acls_out:
        acl_out=conf.acls_v4_out(args=conf.args)
        common_output(acl_out)
        suppress_top_level = True
        
    if not suppress_top_level:
        common_output(conf)

    log_memory("Done")
