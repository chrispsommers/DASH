# saivisor for DASH
Enhance the sai-thrift code generator to surround SAI calls with DTRACE probes (USDT eBPF probes).

# Code Modifications

## Dockerfile.saithrift-bldr
Add packages: `binutils` (for `readelf`) and `systemtap-sdt-dev` (for `<sys/sdt.h>`)

# Build the server
```
chris@chris-z4:~/chris-DASH/DASH/dash-pipeline$ make [p4 sai] saithrift-server
```
## saithrift server code generator developer hints
The saithriftv2 code generator lives inside the OCP SAI repo which appears in DASH repo as `dash-pipeline/SAI/SAI` (as a git submodule). It's a Perl template-based codegen. The location us under the SAI `meta/` directory.

To develop perl codegen templates without rebuilding entire saithrift server each time (slow):
```
make run-saithrift-server-bash
cd /SAI/SAI/meta
perl -Irpc gensairpc.pl -ve
```
Then examine resulting `sai_rpc_server.cpp`; if OK, then exit & `make docker-saithrift-bldr saithrift-server`

# Examine elf file for generated sairpcserver
Examine DASH SAI tracepoints:
```
chris@chris-z4:~/chris-DASH/DASH/dash-pipeline$ readelf -n SAI/rpc/usr/sbin/saiserver |grep -A1 saivisor|grep Name|egrep '(dash|vnet|eni|inbound|outbound|pavalid|vip|direction_lookup)'
    Name: create_dash_acl_group_fn
    Name: create_dash_acl_group_ret
    Name: remove_dash_acl_group_fn
    Name: remove_dash_acl_group_ret
    Name: set_dash_acl_group_attribute_fn
    Name: set_dash_acl_group_attribute_ret
    Name: get_dash_acl_group_attribute_fn
    Name: get_dash_acl_group_attribute_ret
    Name: create_dash_acl_rule_fn
    Name: create_dash_acl_rule_ret
    Name: remove_dash_acl_rule_fn
    Name: remove_dash_acl_rule_ret
    Name: set_dash_acl_rule_attribute_fn
    Name: set_dash_acl_rule_attribute_ret
    Name: get_dash_acl_rule_attribute_fn
    Name: get_dash_acl_rule_attribute_ret
    Name: create_direction_lookup_entry_fn
    Name: create_direction_lookup_entry_ret
    Name: remove_direction_lookup_entry_fn
    Name: remove_direction_lookup_entry_ret
    Name: set_direction_lookup_entry_attribute_fn
    Name: set_direction_lookup_entry_attribute_ret
    Name: get_direction_lookup_entry_attribute_fn
    Name: get_direction_lookup_entry_attribute_ret
    Name: create_eni_ether_address_map_entry_fn
    Name: create_eni_ether_address_map_entry_ret
    Name: remove_eni_ether_address_map_entry_fn
    Name: remove_eni_ether_address_map_entry_ret
    Name: set_eni_ether_address_map_entry_attribute_fn
    Name: set_eni_ether_address_map_entry_attribute_ret
    Name: get_eni_ether_address_map_entry_attribute_fn
    Name: get_eni_ether_address_map_entry_attribute_ret
    Name: create_eni_fn
    Name: create_eni_ret
    Name: remove_eni_fn
    Name: remove_eni_ret
    Name: set_eni_attribute_fn
    Name: set_eni_attribute_ret
    Name: get_eni_attribute_fn
    Name: get_eni_attribute_ret
    Name: create_inbound_routing_entry_fn
    Name: create_inbound_routing_entry_ret
    Name: remove_inbound_routing_entry_fn
    Name: remove_inbound_routing_entry_ret
    Name: set_inbound_routing_entry_attribute_fn
    Name: set_inbound_routing_entry_attribute_ret
    Name: get_inbound_routing_entry_attribute_fn
    Name: get_inbound_routing_entry_attribute_ret
    Name: create_outbound_ca_to_pa_entry_fn
    Name: create_outbound_ca_to_pa_entry_ret
    Name: remove_outbound_ca_to_pa_entry_fn
    Name: remove_outbound_ca_to_pa_entry_ret
    Name: set_outbound_ca_to_pa_entry_attribute_fn
    Name: set_outbound_ca_to_pa_entry_attribute_ret
    Name: get_outbound_ca_to_pa_entry_attribute_fn
    Name: get_outbound_ca_to_pa_entry_attribute_ret
    Name: create_outbound_routing_entry_fn
    Name: create_outbound_routing_entry_ret
    Name: remove_outbound_routing_entry_fn
    Name: remove_outbound_routing_entry_ret
    Name: set_outbound_routing_entry_attribute_fn
    Name: set_outbound_routing_entry_attribute_ret
    Name: get_outbound_routing_entry_attribute_fn
    Name: get_outbound_routing_entry_attribute_ret
    Name: create_vip_entry_fn
    Name: create_vip_entry_ret
    Name: remove_vip_entry_fn
    Name: remove_vip_entry_ret
    Name: set_vip_entry_attribute_fn
    Name: set_vip_entry_attribute_ret
    Name: get_vip_entry_attribute_fn
    Name: get_vip_entry_attribute_ret
    Name: create_vnet_fn
    Name: create_vnet_ret
    Name: remove_vnet_fn
    Name: remove_vnet_ret
    Name: set_vnet_attribute_fn
    Name: set_vnet_attribute_ret
    Name: get_vnet_attribute_fn
    Name: get_vnet_attribute_ret
```
Examine all SAI tracepoints (1048 entries at this writing):
```
chris@chris-z4:~/chris-DASH/DASH/dash-pipeline$ readelf -n SAI/rpc/usr/sbin/saiserver |grep -A1 saivisor|grep Name
    Name: create_acl_table_fn
    Name: create_acl_table_ret
    Name: remove_acl_table_fn
    Name: remove_acl_table_ret
...
    Name: set_wred_attribute_fn
    Name: set_wred_attribute_ret
    Name: get_wred_attribute_fn
    Name: get_wred_attribute_ret
```

# Use bpftrace to list usdt probes in running saithrift-server
```
make run-switch             # console 1
make run-saithrift-server   # console 2
```
root@chris-z4:/home/chris/chris-DASH/DASH/dash-pipeline# find /proc/`pidof saiserver`/root/ -name saiserver
/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver
/proc/1165426/root/SAI/rpc/usr/sbin/saiserver

root@chris-z4:/home/chris/chris-DASH/DASH/dash-pipeline# bpftrace -l 'usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver'|egrep '(dash|vnet|eni|inbound|outbound|pavalid|vip|direction_lookup)'
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_dash_acl_group_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_dash_acl_group_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_dash_acl_group_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_dash_acl_group_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_dash_acl_group_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_dash_acl_group_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_dash_acl_group_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_dash_acl_group_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_dash_acl_rule_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_dash_acl_rule_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_dash_acl_rule_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_dash_acl_rule_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_dash_acl_rule_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_dash_acl_rule_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_dash_acl_rule_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_dash_acl_rule_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_eni_ether_address_map_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_eni_ether_address_map_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_eni_ether_address_map_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_eni_ether_address_map_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_eni_ether_address_map_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_eni_ether_address_map_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_eni_ether_address_map_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_eni_ether_address_map_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_eni_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_eni_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_eni_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_eni_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_eni_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_eni_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_eni_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_eni_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_inbound_routing_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_inbound_routing_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_inbound_routing_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_inbound_routing_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_inbound_routing_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_inbound_routing_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_inbound_routing_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_inbound_routing_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_outbound_ca_to_pa_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_outbound_ca_to_pa_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_outbound_ca_to_pa_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_outbound_ca_to_pa_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_outbound_ca_to_pa_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_outbound_ca_to_pa_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_outbound_ca_to_pa_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_outbound_ca_to_pa_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_outbound_routing_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_outbound_routing_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_outbound_routing_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_outbound_routing_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_outbound_routing_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_outbound_routing_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_outbound_routing_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_outbound_routing_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_vip_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_vip_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_vip_entry_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_vip_entry_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_vip_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_vip_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_vip_entry_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_vip_entry_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_vnet_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_create_vnet_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_vnet_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_remove_vnet_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_vnet_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_set_vnet_attribute_ret
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_vnet_attribute_fn
usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver:saivisor:sai_get_vnet_attribute_ret
```
