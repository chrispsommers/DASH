#!/usr/bin/python3
# This is not a test-case. It is a coding technique demonstration.
# We show two ways of creating arrays:
# 1. Using list comprehension; Python expands the array in-memory
# 2. Using a generator. Pythong calls it repeatedly to iterate
#    through all items. Only one is created in memory at a time.
# Both have their advantages.
#
# To run: python3 <filename.py> or just <./filename.py>

def vip_inflate(m,n):
    """
    Return a populated array of vip dictionary entries from m to n-1
    Uses list comphrehension.
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
    Return an sequence of vip dictionary entries from m to n-1
    using generator (yield) technique. Only one element exists in memory at a time.
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

if __name__ == '__main__':
    # vips is a fully-populated array of vip entries
    m=1
    n=10
    print ("Expand VIP entries %d-%d in-memory and print:" % (m,n))
    print ("======================================================\n")
    for vip in vip_inflate(m,n+1):
        print (vip, '\n')

    m=101
    n=110
    print ("Generate VIP entries %d-%d on-the-fly and print:" % (m,n))
    print ("=========================================\n")
    for vip in vip_generate(m,n+1):
        print (vip, '\n')

    print ("Generate VIP removals %d-%d and print:" % (n,m))
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(m,n+1)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
