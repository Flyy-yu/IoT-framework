import pyshark
import math
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# This is the client class, using the MAC address as the identifier
class Client_loc:
    def __init__(self, mac_address):
        self.mac = mac_address

    # Get the list of packet that sent out from one client
    def get_client_list(self, pcap_name):
        client_array = []
        packets = pyshark.FileCapture(pcap_name)
        for pkt in packets:
            try:
                fields = pkt.wlan._all_fields
            except AttributeError:
                continue
            if 'wlan.sa_resolved' in fields:
                if fields['wlan.sa_resolved'] == self.mac:
                    client_array.append(pkt)

    # Get the average dbm value across different packet which sent out from this client.
    def calc_dbm(self, pcap_name):
        dbm_array = []
        packets = pyshark.FileCapture(pcap_name)
        for pkt in packets:
            try:
                fields = pkt.wlan._all_fields
            except AttributeError:
                continue
            if 'wlan.sa_resolved' in fields:
                if fields['wlan.sa_resolved'] == self.mac:
                    try:
                        dbm_array.append(float(pkt.wlan_radio.signal_dbm))
                    except AttributeError:
                        continue

        if len(dbm_array) > 0:
            return sum(dbm_array) / float(len(dbm_array))
        else:
            return 0

            # freq in MHz  5G  = 5180MHz

    def calc_distance(self, dBm, freq):
        # https: // www.everythingrf.com / rf - calculators / free - space - path - loss - calculatorz
        # https://stackoverflow.com/questions/11217674/how-to-calculate-distance-from-wifi-router-using-signal-strength

        # public double calculateDistance(double signalLevelInDb, double freqInMHz) {
        #    double exp = (27.55 - (20 * Math.log10(freqInMHz)) + Math.abs(signalLevelInDb)) / 20.0;
        #    return Math.pow(10.0, exp);
        # }

        # distance = 10 ^ ((27.55 - (20 * log10(frequency)) + signalLevel)/20)
        exp = (27.55 - (20 * math.log10(freq)) + abs(dBm)) / 20
        return 10 ** (exp)


if __name__ == "__main__":
    test = Client_loc('58:e2:8f:9b:6d:5d')
    dBm_value = test.calc_dbm('far.pcap')
    distance = test.calc_distance(dBm_value, 5180)
    print("The distance is: " + str(distance) + " meters") # real distance is about 6.5 meters
    print("The average dBm value is: " + str(dBm_value))

    dBm_value = test.calc_dbm('close.pcap')
    distance = test.calc_distance(dBm_value, 5180)
    print("The distance is: " + str(distance) + " meters") # real distance is about 0.4 meters
    print("The average dBm value is: " + str(dBm_value))