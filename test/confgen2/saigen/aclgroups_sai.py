#!/usr/bin/python3

from confbase import *
from confutils import *
from copy import deepcopy
from aclgroups import *

class AclGroups_Sai(AclGroups):

    class AclRulesIpv4(AclGroups.AclRulesIpv4):
        # Note - not efficient, better to fix dashgen generator to emit 4 different rules
        def __init__(self, params={}, args=None):
            super().__init__(params, args)

            # note somehow during serialization of top-level ACLgroups,
            # some rules contain True/False and some contain 'true'/'false'
            self.map_action_to_sai = {
                'deny': {
                    False:'SAI_DASH_ACL_RULE_ACTION_DENY',
                    'false':'SAI_DASH_ACL_RULE_ACTION_DENY',
                    True:'SAI_DASH_ACL_RULE_ACTION_PERMIT_AND_CONTINUE',
                    'true':'SAI_DASH_ACL_RULE_ACTION_PERMIT_AND_CONTINUE'
                }, 
                'allow': {
                    False:'SAI_DASH_ACL_RULE_ACTION_DENY',
                    'false':'SAI_DASH_ACL_RULE_ACTION_DENY',
                    True:'SAI_DASH_ACL_RULE_ACTION_DENY_AND_CONTINUE',
                    'true':'SAI_DASH_ACL_RULE_ACTION_DENY_AND_CONTINUE'
                }
            }
        
        
        def renderItem(self, item):
            """ Permute src/dst lists"""
            for src in item['src_addrs']:
                for dst in item['dst_addrs']:
                    yield {
                        "type" : "SAI_OBJECT_TYPE_DASH_ACL_RULE",
                        "attributes" : {
                            "SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID" : "from-parent",
                            "SAI_DASH_ACL_RULE_ATTR_PRIORITY" : item['priority'],
                            "SAI_DASH_ACL_RULE_ATTR_ACTION" : \
                                self.map_action_to_sai[item['action']][item['terminating']],
                            "SAI_DASH_ACL_RULE_ATTR_DIP" : dst,
                            "SAI_DASH_ACL_RULE_ATTR_SIP" : src,
                            "SAI_DASH_ACL_RULE_ATTR_PROTOCOL" : "TBD - optional?",
                            "SAI_DASH_ACL_RULE_ATTR_SRC_PORT" : "TBD - optional?",
                            "SAI_DASH_ACL_RULE_ATTR_DST_PORT" : "TBD - optional?",
                            "SAI_DASH_ACL_RULE_ATTR_COUNTER_ID" : "TODO"
                        }
                }
    
    def renderItem(self, item):
        """Remove one list level and populate acl group ID"""
        for k,v in item.items(): #iterate over dict
            rules = list(v['rules']) # extra list level, will remove
            new_rules=[]
            for rule in rules[0]:
                rule['attributes']['SAI_DASH_ACL_RULE_ATTR_DASH_ACL_GROUP_ID']=v['acl-group-id']
                new_rules.append(rule)
            v['rules']=new_rules
        return item

if __name__ == "__main__":
    conf=AclGroups_Sai()
    conf.main()
