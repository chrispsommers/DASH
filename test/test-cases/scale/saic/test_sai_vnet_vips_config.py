# Demonstration of how to generate many config objects with simple generator expressions
import json
import time
from pathlib import Path
from pprint import pprint

import pytest
# import saichallenger.dataplane.snappi.snappi_traffic_utils as stu
# from saichallenger.dataplane.ptf_testutils import (send_packet,
#                                                    simple_udp_packet,
#                                                    simple_vxlan_packet,
#                                                    verify_no_other_packets,
#                                                    verify_packet)

# Constants
SWITCH_ID = 5

# Below the array is expanded in-place by Python interpreter
# using "list comprehension." The entire array sits in memory.
# This is OK for smaller configs.

def vip_inflate(m,n):
    """
    Return a populated array of vip dictionary entries from m to n-1
    """
    return [
        {
            "name": "vip_entry%02d" % x,
            "op": "create",
            "type": "SAI_OBJECT_TYPE_VIP_ENTRY",
            "key": {
            "switch_id": "$SWITCH_ID",
            "vip": "192.168.0.%d" % x
            },
            "attributes": [
            "SAI_VIP_ENTRY_ATTR_ACTION",
            "SAI_VIP_ENTRY_ACTION_ACCEPT"
            ]
        } for x in range (m,n)]

def vip_generate(m,n):
    """
    Return an siterable equence of vip dictionary entries from m to n-1
    using generator (yield) technique. Only one element exists in memory at a time.
    NOTE: m,n sequence is applied to last byte if IP address so m,n limited to (1,256) range
    """
    for x in range (m,n):
        yield \
        {
            "name": "vip_entry%02d" % x,
            "op": "create",
            "type": "SAI_OBJECT_TYPE_VIP_ENTRY",
            "key": {
            "switch_id": "$SWITCH_ID",
            "vip": "192.168.0.%d" % x
            },
            "attributes": [
            "SAI_VIP_ENTRY_ATTR_ACTION",
            "SAI_VIP_ENTRY_ACTION_ACCEPT"
            ]
        }
    return

vip_start=1
vip_end=255

# @pytest.mark.ptf
# @pytest.mark.snappi
class TestSaiDashVips:
    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vips_create(self, dpu):
        """Verify VIP configuration create
           array is generated on the fly
        """
        result = [*dpu.process_commands( (vip_generate(vip_start,vip_end+1)) )]
        print("\n======= SAI commands RETURN values =======")
        pprint(result)

    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vips_remove(self, dpu):
        """Verify VIP configuration removal
           Entries generated and modifed on the fly; added to array in memory; reversed; then executed.
        """
        cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start,vip_end+1)]
        cleanup_commands = reversed(cleanup_commands)

        result = [*dpu.process_commands(cleanup_commands)]
        # print("\n======= SAI commands RETURN values =======")
        # pprint(result)
