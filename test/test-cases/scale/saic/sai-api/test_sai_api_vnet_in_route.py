import json
import time
from pathlib import Path
from pprint import pprint

import pytest
import saichallenger.dataplane.snappi.snappi_traffic_utils as stu
from saichallenger.dataplane.ptf_testutils import (send_packet,
                                                   simple_udp_packet,
                                                   simple_vxlan_packet,
                                                   verify_no_other_packets,
                                                   verify_packet)

import dash_helper.vnet2vnet_helper as dh

current_file_dir = Path(__file__).parent

# Constants
SWITCH_ID = 5
eni_id = 1


class TestSaiVnetInboundRoutingEntry:

    def test_vnet_inbound_routing_entry_create(self, dpu):

        commands = [
            {
                "name": "inbound_routing_entry",
                "op": "create",
                "type": "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
                "key": {
                    "switch_id": "$SWITCH_ID",
                    "eni_id": "$eni_id",
                    "vni": "1000",
                    "sip": "10.10.2.0",
                    "sip_mask": "255.255.255.0",
                    "priority": 0
                },
                "attributes": [
                    "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION",
                    "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_PA_VALIDATE",
                    "SAI_INBOUND_ROUTING_ENTRY_ATTR_SRC_VNET_ID",
                    "$vnet_1"
                ]
            },
        ]
        result = [*dpu.process_commands(commands)]
        print("\n======= SAI commands RETURN values create =======")
        pprint(result)

    # TODO: Expand verification for get and set for all attributes
    def test_vnet_inbound_routing_entry_get1(self, dpu):

        commands = [
            {
                "name": "inbound_routing_entry",
                "op": "get",
                "type": "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
                "attribute": "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION"
            }
        ]
        result = [*dpu.process_commands(commands)]
        print("\n======= SAI commands RETURN values get =======")
        pprint(result)

        assert (result[0].value(),
                "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_PA_VALIDATE")

    # TODO: figure out all supported values for set attributes
    def test_vnet_inbound_routing_entry_set(self, dpu):

        commands = [
            {
                "name": "inbound_routing_entry",
                "op": "set",
                "type": "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
                "key": {
                    "switch_id": "$SWITCH_ID",
                    "eni_id": "$eni_id",
                    "vni": "2000",
                    "sip": "10.10.10.0",
                    "sip_mask": "255.255.255.0",
                    "priority": 0
                },
                "attribute": [
                    "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION",
                    "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_CA_VALIDATE",
                ]
            },
        ]
        result = [*dpu.process_commands(commands)]
        print("\n======= SAI commands RETURN values set =======")
        pprint(result)

    # TODO: Expand verification for get and set for all attributes
    def test_vnet_inbound_routing_entry_get2(self, dpu):

        commands = [
            {
                "name": "$vnet",
                "op": "get",
                "type": "SAI_OBJECT_TYPE_VNET",
                "attribute": "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION"
            }
        ]
        result = [*dpu.process_commands(commands)]
        print("\n======= SAI commands RETURN values get =======")
        pprint(result)

        assert (result[0].value(),
                "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_CA_VALIDATE")

    def test_vnet_inbound_routing_entry_remove(self, dpu):

        commands = [
            {
                "name": "inbound_routing_entry",
                "op": "remove",
                "type": "SAI_OBJECT_TYPE_INBOUND_ROUTING_ENTRY",
                "key": {
                    "switch_id": "$SWITCH_ID",
                    "eni_id": "$eni_id",
                    "vni": "1000",
                    "sip": "10.10.10.0",
                    "sip_mask": "255.255.255.0",
                    "priority": 0
                },
                "attributes": [
                    "SAI_INBOUND_ROUTING_ENTRY_ATTR_ACTION",
                    "SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_PA_VALIDATE",
                    "SAI_INBOUND_ROUTING_ENTRY_ATTR_SRC_VNET_ID",
                    "$vnet_1"
                ]
            },
        ]

        result = [*dpu.process_commands(commands)]
        print("\n======= SAI commands RETURN values remove =======")
        pprint(result)
