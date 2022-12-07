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
# This is OK for smaller configs and simple loop expressions.
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

def vip_generate(vip_start=1, a1=192, a2=192, b1=168, b2=168, c1=0, c2=0, d1=1, d2=1):
    """
    Return an sequence of vip dictionary entries with incrementing IP addresses.
    Uses generator (yield) technique. Only one element exists in memory at a time.
    A sequence is generated with least-significant IP address octets incrementing first,
    followed by successive outer octets. So, for the IP adddress A.B.C.D, D counts the quickest,
    A counts the slowest.
    vip_start - starting VIP number, successive entries will increment this by 1
    a1, a2 - starting, ending values (inclusive) for address octet "A" in the sequence A.B.C.D
    b1, b2 - starting, ending values (inclusive) for address octet "B" in the sequence A.B.C.D
    c1, c2 - starting, ending values (inclusive) for address octet "C" in the sequence A.B.C.D
    d1, d2 - starting, ending values (inclusive) for address octet "D" in the sequence A.B.C.D
    """
    v = vip_start
    for a in range (a1,a2+1):
        for b in range(b1, b2+1):
            for c in range(c1,c2+1):
                for d in range(d1,d2+1):
                    yield \
                    {
                        "name": "vip_entry%d" % v,
                        "op": "create",
                        "type": "SAI_OBJECT_TYPE_VIP_ENTRY",
                        "key": {
                        "switch_id": "$SWITCH_ID",
                        "vip": "%d.%d.%d.%d" % (a,b,c,d)
                        },
                        "attributes": [
                        "SAI_VIP_ENTRY_ATTR_ACTION",
                        "SAI_VIP_ENTRY_ACTION_ACCEPT"
                        ]
                    }
                    v+= 1
    return


# @pytest.mark.ptf
# @pytest.mark.snappi
class TestSaiDashVips:
    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vips_create(self, dpu):
        """Verify VIP configuration create
           array is generated on the fly
        """
        # create 2x2x2x32 = 256 vips
        result = [*dpu.process_commands( (vip_generate(vip_start=1,a1=192, a2=193, b1=168, b2=169, c1=1,c2=2,d1=1,d2=32)) )]
        print("\n======= SAI commands RETURN values =======")
        pprint(result)

    @pytest.mark.ptf
    @pytest.mark.snappi
    def test_many_vips_remove(self, dpu):
        """Verify VIP configuration removal
           Entries generated and modifed on the fly; added to array in memory; reversed; then executed.
        """
        # remove 2x2x2x32 = 256 vips
        cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=1,a1=192, a2=193, b1=168, b2=169, c1=1,c2=2,d1=1,d2=32)]
        cleanup_commands = reversed(cleanup_commands)

        result = [*dpu.process_commands(cleanup_commands)]
        # print("\n======= SAI commands RETURN values =======")
        # pprint(result)
