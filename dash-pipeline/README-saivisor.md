# saivisor for DASH
Enhance the sai-thrift code generator to surround SAI calls with DTRACE probes (USDT eBPF probes).

# Code Modifications

## Dockerfile.saithrift-bldr
Add packages: `binutils` (for `readelf`) and `systemtap-sdt-dev` (for `<sys/sdt.h>`)

# Build the server
```
chris@chris-z4:~/chris-DASH/DASH/dash-pipeline$ make [p4 sai] saithrift-server
```
# Examine elf file for generated sairpcserver

```
chris@chris-z4:~/chris-DASH/DASH/dash-pipeline$ make docker-saithrift-bldr 

dashuser@chris-z4:/SAI/rpc/usr/sbin$ readelf -n saiserver |egrep sai.*ret|egrep '(dash|vnet|eni|inbound|outbound|pavalid|vip|directionlookip)'
    Name: sai_create_dash_acl_group_ret
    Name: sai_remove_dash_acl_group_ret
    Name: sai_set_dash_acl_group_attribute_ret
    Name: sai_get_dash_acl_group_attribute_ret
    Name: sai_create_dash_acl_rule_ret
    Name: sai_remove_dash_acl_rule_ret
    Name: sai_set_dash_acl_rule_attribute_ret
    Name: sai_get_dash_acl_rule_attribute_ret
    Name: sai_create_eni_ether_address_map_entry_ret
    Name: sai_remove_eni_ether_address_map_entry_ret
    Name: sai_set_eni_ether_address_map_entry_attribute_ret
    Name: sai_get_eni_ether_address_map_entry_attribute_ret
    Name: sai_create_eni_ret
    Name: sai_remove_eni_ret
    Name: sai_set_eni_attribute_ret
    Name: sai_get_eni_attribute_ret
    Name: sai_create_inbound_routing_entry_ret
    Name: sai_remove_inbound_routing_entry_ret
    Name: sai_set_inbound_routing_entry_attribute_ret
    Name: sai_get_inbound_routing_entry_attribute_ret
    Name: sai_create_outbound_ca_to_pa_entry_ret
    Name: sai_remove_outbound_ca_to_pa_entry_ret
    Name: sai_set_outbound_ca_to_pa_entry_attribute_ret
    Name: sai_get_outbound_ca_to_pa_entry_attribute_ret
    Name: sai_create_outbound_routing_entry_ret
    Name: sai_remove_outbound_routing_entry_ret
    Name: sai_set_outbound_routing_entry_attribute_ret
    Name: sai_get_outbound_routing_entry_attribute_ret
    Name: sai_create_vip_entry_ret
    Name: sai_remove_vip_entry_ret
    Name: sai_set_vip_entry_attribute_ret
    Name: sai_get_vip_entry_attribute_ret
    Name: sai_create_vnet_ret
    Name: sai_remove_vnet_ret
    Name: sai_set_vnet_attribute_ret
    Name: sai_get_vnet_attribute_ret
dashuser@chris-z4:/SAI/rpc/usr/sbin$ readelf -n saiserver |egrep sai.*ret|egrep '(dash|vnet|eni|inbound|outbound|pavalid|vip|directionlookip)'|wc
     36      72    1606
```

# Use bpftrace to list usdt probes in running saithrift-server
```
root@chris-z4:/home/chris/chris-DASH/DASH/dash-pipeline# find /proc/`pidof saiserver`/root/ -name saiserver
/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver
/proc/1165426/root/SAI/rpc/usr/sbin/saiserver

root@chris-z4:/home/chris/chris-DASH/DASH/dash-pipeline# bpftrace -l 'usdt:/proc/1165426/root/SAI/SAI/test/saithriftv2/saiserver'|egrep '(dash|vnet|eni|inbound|outbound|pavalid|vip|directionlookip)'
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