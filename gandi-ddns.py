#!/bin/env python3

import re
import sys
import xmlrpc.client
from datetime import datetime, timezone

api_host = 'https://rpc.gandi.net/xmlrpc/'
api_key = 'secret'

def extract_args(args):
    if len(args) != 3:
        print('Usage:', args[0], 'domain', 'ip_addres')
        sys.exit(1)

    domain, ip_address = args[1], args[2]

    if not re.match(r'^\w+\.[\w.]+$', domain):
        raise ValueError('Wrong domain format!');

    if not re.match(r'^[0-2]?\d?\d\.[0-2]?\d?\d\.[0-2]?\d?\d\.[0-2]?\d?\d$', ip_address):
        raise ValueError('Wrong ip address format!');

    return domain, ip_address

def get_time():
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()

if __name__ == '__main__':
    domain, ip_address = extract_args(sys.argv)
    api = xmlrpc.client.ServerProxy(api_host)

    zone_id = api.domain.info(api_key, domain)['zone_id']
    records = [ r['value'] for r in api.domain.zone.record.list(api_key, zone_id, 0, {'name': '@', 'type': 'A'}) ]

    if not records or not all(record == ip_address for record in records):
        new_version = api.domain.zone.version.new(api_key, zone_id)

        print(
            '[{}] Setting {} as new IP address for {} (zone version: {})... '.format(
                get_time(), ip_address, domain, new_version
            ), end=''
        )

        api.domain.zone.record.delete(api_key, zone_id, new_version, {'name': '@', 'type': 'A'})
        api.domain.zone.record.add(api_key, zone_id, new_version, {'name': '@', 'type': 'A', 'value': ip_address})
        api.domain.zone.version.set(api_key, zone_id, new_version)

        print('OK')
