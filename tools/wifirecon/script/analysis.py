import pyshark
import json
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore", category=RuntimeWarning)

packets = pyshark.FileCapture('phone.pcap')


# This is the Device class, it contains attribute like MAC address, number of packer in and out,
# client list and prob list.

# the Vendor lookup class. It load vendor information from vendordb.txt and store information in a dict
class VendorLookup:
    def __init__(self, db_filename):
        self.filename = db_filename
        self.dict = {}
        db = open(db_filename, 'r')
        line = db.readline()
        while line:
            array = line.split('    ')
            line = db.readline()
            try:
                self.dict[array[0]] = array[2][:-1]
            except IndexError:
                continue

    def lookup(self, mac_address):
        vendor_block = mac_address[0:8].upper()
        if vendor_block in self.dict:
            return self.dict[vendor_block]
        else:
            return 'Unknown'


# helper function to load set() in json
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class Device:
    def __init__(self, mac_address):
        self.mac = mac_address
        self.device_type = 'Unknown'
        self.packet_out = 0
        self.packet_in = 0
        self.client_list = set()
        self.prob_list = set()
        self.vendor = ''
        self.AP_info = {}

    # If the device is an access point, call this function
    def set_ap(self, packet):
        self.device_type = 'Access Point'

        try:
            wlan_info = packet[3]
        except IndexError:
            return False
        # Add management information for access point
        try:
            self.AP_info['Frequency'] = str(packet.wlan_radio.frequency) + 'MHz'
            self.AP_info['Channel'] = wlan_info.ds_current_channel
        except AttributeError:
            pass

        try:
            if "SSID:" not in wlan_info.ssid:
                self.AP_info['SSID'] = wlan_info.ssid
        except AttributeError:
            pass

    def check_Apinfo(self):
        return ("SSID" in self.AP_info)

    def set_client(self):
        self.device_type = "Client"

    def increase_in(self):
        self.packet_in = self.packet_in + 1

    def increase_out(self):
        self.packet_out = self.packet_out + 1

    def prob_list_add(self, address):
        # self.device_type = "Client"
        self.prob_list.add(address)

    def client_list_add(self, address):
        self.client_list.add(address)

    def json_output(self, vendor):
        result = {}
        # remove "Fake Mac address"
        if self.packet_in > 1 and self.packet_out > 1:
            if self.device_type == 'Unknown':
                result['Vendor'] = vendor
                result['Device_type'] = self.device_type
                result['frame_sent'] = self.packet_out
                result['frame_received'] = self.packet_in

            elif self.device_type == 'Client':
                result['Vendor'] = vendor
                result['Device_type'] = self.device_type
                result['frame_sent'] = self.packet_out
                result['frame_received'] = self.packet_in
                result['prob_list'] = self.prob_list

            elif self.device_type == 'Access Point':
                if 'ff:ff:ff:ff:ff:ff' in self.client_list:
                    self.client_list.remove('ff:ff:ff:ff:ff:ff')
                result['Vendor'] = vendor
                result['Device_type'] = self.device_type
                result['frame_sent'] = self.packet_out
                result['frame_received'] = self.packet_in
                result['client_list'] = self.client_list
                result['AP_management_info'] = self.AP_info

        return result


# The Analyzer class, it read a pcap file and process every packet in the pcap file.
class Analyzer:
    def __init__(self, pcap):
        self.pcap = pcap
        self.json_output = {}
        self.db = VendorLookup('vendordb.txt')

    def analyze(self):
        print('Processing the Pcap, this mighe take a while...')
        self.packets = pyshark.FileCapture(self.pcap)
        result_dict = {}
        pkt_obj = tqdm(self.packets)
        pkt_count = 0
        for packet in pkt_obj:
            pkt_count += 1
            #display the progress
            pkt_obj.set_description('Processing packet number %d ' % pkt_count)
            try:
                fields = packet.wlan._all_fields
            except AttributeError:
                continue

            #look for bssid
            if 'wlan.bssid_resolved' in fields:
                bssid_mac = (fields['wlan.bssid_resolved'])

                if bssid_mac not in result_dict:
                    AP_device = Device(bssid_mac)
                    AP_device.set_ap(packet)
                    result_dict[bssid_mac] = AP_device
                elif not result_dict[bssid_mac].check_Apinfo():
                    result_dict[bssid_mac].set_ap(packet)

                if 'wlan.ra_resolved' in fields:
                    if fields['wlan.ra_resolved'] != bssid_mac:
                        result_dict[bssid_mac].client_list_add(fields['wlan.ra_resolved'])
                        if fields['wlan.ra_resolved'] in result_dict:
                            result_dict[fields['wlan.ra_resolved']].set_client()
                if 'wlan.sa_resolved' in fields:
                    if fields['wlan.sa_resolved'] != bssid_mac:
                        result_dict[bssid_mac].client_list_add(fields['wlan.sa_resolved'])
                        if fields['wlan.sa_resolved'] in result_dict:
                            result_dict[fields['wlan.sa_resolved']].set_client()

            # look for MAC address of the receiver
            if 'wlan.ra_resolved' in fields:
                if fields['wlan.ra_resolved'] not in result_dict:
                    device_object = Device(fields['wlan.ra_resolved'])
                    device_object.increase_in()
                    result_dict[fields['wlan.ra_resolved']] = device_object
                else:
                    result_dict[fields['wlan.ra_resolved']].increase_in()
                if fields['wlan.fc.type_subtype'] == '5':
                    result_dict[fields['wlan.ra_resolved']].prob_list_add(fields['wlan.sa_resolved'])
            # look for MAC address of the sender
            if 'wlan.sa_resolved' in fields:
                if fields['wlan.sa_resolved'] not in result_dict:
                    device_object = Device(fields['wlan.sa_resolved'])
                    device_object.increase_out()
                    result_dict[fields['wlan.sa_resolved']] = device_object
                else:
                    result_dict[fields['wlan.sa_resolved']].increase_out()
            elif 'wlan.ta_resolved' in fields:
                if fields['wlan.ta_resolved'] not in result_dict:
                    device_object = Device(fields['wlan.ta_resolved'])
                    device_object.increase_out()
                    result_dict[fields['wlan.ta_resolved']] = device_object
                else:
                    result_dict[fields['wlan.ta_resolved']].increase_out()

        # remove broadcast address
        del result_dict['ff:ff:ff:ff:ff:ff']

        for key, value in result_dict.items():
            # loop up vendor base on mac address
            vendor = self.db.lookup(key)
            self.json_output[key] = value.json_output(vendor)
        json_result = json.dumps(self.json_output, cls=SetEncoder, indent=4)
        out_file = open('result.json', 'w')
        out_file.write(json_result)
        out_file.close()
        return json_result


if __name__ == "__main__":
    # testa = Analyzer('alfa.pcap')
    # print(testa.analyze())

    testb = Analyzer('close.pcap')
    print(testb.analyze())
