#!/usr/bin/python3
# This is not a test-case. It is a coding technique demonstration.
# We show two ways of creating arrays:
# 1. Using list comprehension; Python expands the array in-memory
# 2. Using a generator. Pythong calls it repeatedly to iterate
#    through all items. Only one is created in memory at a time.
# Both have their advantages:
# - List comprehensions are OK for simple, non-nested loops without logic and low memory footprint
# - Generators are good for nested loops, complex logic and low memory footprint
#
# To run: python3 <filename.py> or just <./filename.py>

def vip_inflate(m,n):
    """
    Return a populated array of vip dictionary entries from m to n inclusive
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
        } for x in range (m,n+1)]

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

if __name__ == '__main__':
    # vips is a fully-populated array of vip entries
    m=1
    n=10
    print ("Expand VIP entries %d-%d in-memory and print:" % (m,n))
    print ("======================================================\n")
    for vip in vip_inflate(m,n):
        print (vip, '\n')

    
    print ("Generate VIP entries on-the-fly (increment D) and print:")
    print ("=========================================\n")
    for vip in vip_generate(vip_start=100,d1=1,d2=10):
        print (vip, '\n')

    print ("Generate VIP removals (increment D) and print:")
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=100,d1=1,d2=10)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
    
    print ("Generate VIP entries on-the-fly (increment C) and print:")
    print ("=========================================\n")
    for vip in vip_generate(vip_start=200,c1=1,c2=10):
        print (vip, '\n')

    print ("Generate VIP removals (increment C) and print:")
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=200,c1=1,c2=10)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
    
    print ("Generate VIP entries on-the-fly (increment B) and print:")
    print ("=========================================\n")
    for vip in vip_generate(vip_start=300,b1=168,b2=177):
        print (vip, '\n')

    print ("Generate VIP removals (increment B) and print:")
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=300,b1=168,b2=177)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
    
    print ("Generate VIP entries on-the-fly (increment A) and print:")
    print ("=========================================\n")
    for vip in vip_generate(vip_start=400,a1=192,a2=199):
        print (vip, '\n')

    print ("Generate VIP removals (increment A) and print:")
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=400,a1=192,a2=199)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
    
    print ("Generate VIP entries on-the-fly (increment A,B,C,D) and print:")
    print ("=========================================\n")
    for vip in vip_generate(vip_start=1001,a1=192, a2=193, b1=168, b2=169, c1=1,c2=2,d1=1,d2=255):
        print (vip, '\n')

    print ("Generate VIP removals (increment A,B,C,D) and print:")
    print ("=========================================\n")

    cleanup_commands = [{'name': vip['name'], 'op': 'remove'} for vip in vip_generate(vip_start=1001,a1=192, a2=193, b1=168, b2=169, c1=1,c2=2,d1=1,d2=255)]
    cleanup_commands = reversed(cleanup_commands)
    for vip in cleanup_commands:
        print (vip, '\n')
