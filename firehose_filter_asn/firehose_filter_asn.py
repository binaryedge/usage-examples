import json
import requests
from netaddr import IPSet

# Fill in your BinaryEdge Token here
BE_TOKEN = 'XXX'

# Fill in your ASN query here, can be a name (i.e, 'google') or a AS number (i.e, '12345')
ASN_QUERY = '12345'

# initialize the set of IP addresses that we want to filter
ip_set = IPSet()

# request all ASNs matching a NAME OR NUMBER
response = requests.get('https://geoip.services.core.binaryedge.io/asn/' + ASN_QUERY,
                        headers={'X-Token': BE_TOKEN})
parsed_response = json.loads(response.text)

# add all addresses to the set of IP addresses
for entry in parsed_response:
    ip_set |= IPSet(entry['as_prefixes'])

# get from firehose endpoint (streaming endpoint, hence stream=True)
response = requests.get('https://api.binaryedge.io/v1/firehose',
                        headers={'X-Token': BE_TOKEN}, stream=True)

# for each event, check the IP address and check if it matches our list
for line in response.iter_lines():
    parsed_line = json.loads(line)
    if parsed_line['target']['ip'] in ip_set:
        print(json.dumps(parsed_line))
