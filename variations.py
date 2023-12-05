from table.activity import Activity
from table.fqdn import FQDN
from table.ip_address import IPAddress

from util.lookup import Resolve
from util.whois import Whois

class Application:

    activity = None

    fqdn = None

    ip_address = None

    resolve = None

    whois = None

    def __init__(self):
        self.activity = Activity()

        self.fqdn = FQDN()

        self.ip_address = IPAddress()

        self.resolve = Resolve()

        self.whois = Whois()

    def process(self):
        # list of ips to check
        total_ip_addresses = self.get_clean_ip_addresses()

        total_fqdns = self.get_clean_fqdns()

        print(total_fqdns)
        exit()

        # list of grouped variations
        grouped_variations = self.get_grouped_variations()

        # loop through variations
        for key in grouped_variations:
            print(f"    -> {key}")

            # loop through iptvs under single variation
            for iptv in grouped_variations[key]:
                variated_fqdns = []

                # loop through iptvs' fqdn
                for fqdn_record_id in iptv['fields']['FQDN']:
                    single_fqdn_record = self.fqdn.get_record(fqdn_record_id)

                    if 'Univocal IP Address' in single_fqdn_record['fields'].keys():
                        resolved_ip_address = self.resolve.fqdn(single_fqdn_record['fields']['FQDN'])

                        # if empty, go on
                        if not resolved_ip_address:
                            continue

                        # if already in the ip addresses list, go on
                        if resolved_ip_address in total_ip_addresses:
                            continue

                        # if not changed, go on
                        if single_fqdn_record['fields']['Univocal IP Address'][0] == resolved_ip_address:
                            continue

                        if self.check_unwanteds(single_fqdn_record['fields']['FQDN']):
                            continue

                        single_variated_iptv = {
                            'fqdn': single_fqdn_record['fields']['FQDN'],
                            'old_ip_address': single_fqdn_record['fields']['Univocal IP Address'][0],
                            'new_ip_address': resolved_ip_address
                        }

                        # TODO: check ip nearbies on security trails

                        # TODO: build list of fqdns on airtable

                        variated_fqdns.append(single_variated_iptv)

                if variated_fqdns:
                    print(f"    - {iptv['fields']['IPTV Name VARIATION'][0]}")

                    for variated_fqdn in variated_fqdns:
                        print(f"        {variated_fqdn['fqdn']} ({variated_fqdn['old_ip_address']} -> {variated_fqdn['new_ip_address']})")

    def get_grouped_variations(self):
        variations = self.activity.get_variations()

        grouped_records = {}

        # grouping records by Serie/Season/Day
        for record in variations.get("records", []):
            # field Serie/Season/Day
            group_field_value = record["fields"].get("Serie/Season/Day")[0]

            if group_field_value in list(grouped_records.keys()):
                grouped_records[group_field_value].append(record)

            else:
                grouped_records[group_field_value] = [record]

        return grouped_records

    # [ '1.2.3.4', '1.1.1.1', .. ]
    def get_clean_ip_addresses(self):
        records = self.ip_address.get_records()

        return self.get_only_field(records, 'IP Address')

    def get_clean_fqdns(self):
        records = self.fqdn.get_total()

        return self.get_only_field(records, 'Fully Qualified Domain Name')

    def get_only_field(self, data: dict, field: str):
        clean_records = []

        for record in data.get("records", []):
            if field in record['fields'].keys():
                clean_records.append(record['fields'][field])

        return clean_records

    def check_unwanteds(self, value):
        result = self.whois.get_text(value)

        result = result.lower()

        if 'cloudflare' in result or 'namecheap' in result or 'amazon' in result or 'google' in result:
            return True

        return False

a = Application()

a.process()
