#!/usr/bin/python3

from confbase import *
from confutils import *
from enis import *

class Enis_Sai(Enis):

    def __init__(self, params={}, args=None):
        super().__init__(params, args)
        self.acl_in = self.AclsV4In(self.params)
        self.acl_out = self.AclsV4Out(self.params)
        self.subgens = [self.acl_in, self.acl_out]

    class AclsV4In(Enis.AclsV4In):

        def renderItem(self,item):
            # Note below is just example, can modify to suit
            return { "in_acl_group": {
                            "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
                            "attributes" : {
                                "SAI_DASH_ACL_GROUP_ATTR_IP_ADDR_FAMILY" : "SAI_IP_ADDR_FAMILY_IPV4"
                            }
                        }   
            }
            # return 'sai_thrift_create_dash_acl_group(self.client, ip_addr_family=SAI_IP_ADDR_FAMILY_IPV4)'

    class AclsV4Out(Enis.AclsV4Out):

        def renderItem(self,item):
            # Note below is just example, can modify to suit
            return { "in_acl_group": {
                            "type" : "SAI_OBJECT_TYPE_DASH_ACL_GROUP",
                            "attributes" : {
                                "SAI_DASH_ACL_GROUP_ATTR_IP_ADDR_FAMILY" : "SAI_IP_ADDR_FAMILY_IPV4"
                            }
                        }   
            }
            # return 'sai_thrift_create_dash_acl_group(self.client, ip_addr_family=SAI_IP_ADDR_FAMILY_IPV4)'

    def renderItem(self,item):
        # Note below is just example, can modify to suit
        return {
            "eni_id" : {
                "type" : "SAI_OBJECT_TYPE_ENI",
                "attributes" : {
                    "SAI_ENI_ATTR_CPS" : "10000",
                    "SAI_ENI_ATTR_PPS" : "100000",
                    "SAI_ENI_ATTR_FLOWS" : "100000",
                    "SAI_ENI_ATTR_ADMIN_STATE" : "True",
                    "SAI_ENI_ATTR_VM_UNDERLAY_DIP" : "vm_underlay_dip",
                    "SAI_ENI_ATTR_VM_VNI" : "9",
                    "SAI_ENI_ATTR_VNET_ID" : "self.vnet_id",
                    "SAI_ENI_ATTR_INBOUND_V4_STAGE1_DASH_ACL_GROUP_ID" : "self.in_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V4_STAGE2_DASH_ACL_GROUP_ID" : "self.in_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V4_STAGE3_DASH_ACL_GROUP_ID" : "self.in_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V4_STAGE4_DASH_ACL_GROUP_ID" : "self.in_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V4_STAGE5_DASH_ACL_GROUP_ID" : "self.in_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V6_STAGE1_DASH_ACL_GROUP_ID" : "self.out_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V6_STAGE2_DASH_ACL_GROUP_ID" : "self.out_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V6_STAGE3_DASH_ACL_GROUP_ID" : "self.out_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V6_STAGE4_DASH_ACL_GROUP_ID" : "self.out_acl_group_id",
                    "SAI_ENI_ATTR_INBOUND_V6_STAGE5_DASH_ACL_GROUP_ID" : "self.out_acl_group_id",
                    "SAI_ENI_ATTR_OUTBOUND_V4_STAGE1_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V4_STAGE2_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V4_STAGE3_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V4_STAGE4_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V4_STAGE5_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V6_STAGE1_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V6_STAGE2_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V6_STAGE3_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V6_STAGE4_DASH_ACL_GROUP_ID" : "0",
                    "SAI_ENI_ATTR_OUTBOUND_V6_STAGE5_DASH_ACL_GROUP_ID" : "0"
                }
            }
        }

if __name__ == "__main__":

    conf=Enis_Sai()
    conf.main()
