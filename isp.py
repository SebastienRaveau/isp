#! /usr/bin/env python

import os
import sys
import time
import random
from scapy.all import *


conf.verb = 0
dns_server = sys.argv[1] if 2 == len(sys.argv) else 'resolver1.opendns.com'
wildcard_tlds = ['cg', 'cm', 'kr', 'mp', 'nu', 'ph', 'rw', 'st', 'tk', 'vg', 'ws']


def str2qd(fqdn):
    qd = ''
    for n in fqdn.split('.'):
        qd += chr(len(n)) + n
    qd += '\x00\x00\x01\x00\x01'
    return qd


def improbable_domain():
    fqdn = ''
    while len(fqdn) < 200:
        fqdn += str(random.random()) + '.'
    return fqdn


def random_iana_ip():
    ip = '42.' + str(random.randint(0, 254))
    ip += '.' + str(random.randint(0, 254))
    ip += '.' + str(random.randint(1, 254))
    return ip


def get_ttl(fqdn, spoof_source):
    i = IP()
    u = UDP(dport = 53)
    d = DNS(qr = 0, opcode = 0, rd = 1, qdcount = 1)
    i.dst = dns_server
    d.id = random.randint(0, 65535)
    d.qd = str2qd(fqdn)
    if spoof_source:
        i.src = random_iana_ip()
    res = sr1(i/u/d, timeout = 3)
    try:
        return res.an.ttl
    except:
        return 0


print 'isp.py: "I Spoof Packets with my ISP", by Sebastien Raveau'
print 'Usage: ' + sys.argv[0] + ' [alternate DNS server on the Internet]\n'


if os.geteuid() != 0:
    print 'This script has to be run as root, sorry.'
    sys.exit(1)


print 'WARNING: this gives false-positives when run behind some NAT'
print 'routers! If anybody has an idea of how to prevent that, please'
print 'leave a comment under the blog post explaing how this tool works:'
print 'http://blog.sebastien.raveau.name/2009_02_01_archive.html\n'


for tld in random.sample(wildcard_tlds, 5):
    default_ttl = get_ttl(improbable_domain() + tld, 0)
    if 0 == default_ttl:
        print 'Failed to reach DNS server at ' + dns_server
        print 'Try again or try ' + sys.argv[0] + ' <other-DNS-server>'
        sys.exit(3)
    print 'Default TTL for .' + tld + ': ' + str(default_ttl)
    challenge = improbable_domain() + tld
    if 0 != get_ttl(challenge, 1):
        print 'Your ISP enforces your address on spoofed packets'
        sys.exit(4)
    ttl = get_ttl(challenge, 0)
    print 'TTL 2 seconds after spoofed DNS query: ' + str(ttl)
    if ttl != default_ttl:
        print '\nOur spoofed packets went through!'
        sys.exit(0)
print '\nYour ISP drops spoofed IP packets.'
sys.exit(5)
