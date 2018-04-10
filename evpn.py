import socket
import struct

# some handy routine to convert cidr to netmask
def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return network, netmask

# now build vars to apply to jinja2 template
def create_evpn_vars(cust_vars):
    customer = {}

    (customer['ipv4'], customer['netmask']) = cidr_to_netmask(cust_vars['ipv4'])

    # not all customers have ipv6 enabled.
    if 'ipv6' in cust_vars:
        (customer['ipv6'], customer['prefix']) = cust_vars['ipv6'].split('/')

    customer['bvi'] = "BVI{}".format(cust_vars['evi'])
    customer['description'] = "interface for customer {}".format(cust_vars['name'])
    customer['evi'] = cust_vars['evi']
    customer['name'] = cust_vars['name']

    # we're going to build a loop in jinja template, just add connected_interfaces
    customer['connected_interfaces'] = cust_vars['connected_interfaces']

    # now return dictionary with our vars to create config
    return customer

# now create unique mac addres based on EVI
def create_mac(evi):
    # first make sure evi is a int and convert to hex
    # then strip 0x and fill with 4 chars.
    mac = hex(int(evi))[2:].zfill(4)

    # the spit in half and add : in between
    final_mac = "{}:{}".format(mac[:len(mac) / 2], mac[len(mac) / 2:])

    return final_mac