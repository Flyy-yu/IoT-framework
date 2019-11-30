apt-get -y update
apt-get install -y vim
apt-get install -y openssh-server
apt-get install -y hydra
apt-get install -y binwalk
apt-get install -y git
apt-get install -y python-pip
apt-get install -y python3-pip
apt-get install -y default-jre
apt-get install -y default-jdk
apt-get install -y cmake libusb-1.0-0-dev make gcc g++ libbluetooth-dev pkg-config libpcap-dev python-numpy python-pyside python-qt4
apt-get install -y minicom
apt-get install -y python3-pip
apt-get install -y libglib2.0-dev
apt-get install -y npm
apt-get install -y python-gtk2 python-cairo python-usb python-crypto python-serial python-dev libgcrypt-dev
apt-get install -y git build-essential zlib1g-dev liblzma-dev python-magic
apt-get install -y libssl-dev libevent-dev
apt-get install -y dsniff
apt-get install -y socat
apt-get install -y aircrack-ng
apt-get install -y libcurl4-gnutls-dev
apt-get install -y android-tools-adb android-tools-fastboot
apt-get install -y python-dnspython
sudo pip install boofuzz
sudo pip3 install scapy
sudo pip install scapy
sudo pip3 install pyshark
sudo pip install pyshark
sudo pip install capstone
sudo pip install colorama
sudo pip install frida-tools
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
cd ~/Desktop
git clone https://github.com/Flyy-yu/IoT-framework.git
git clone https://github.com/maurosoria/dirsearch.git
git clone https://github.com/maaaaz/webscreenshot.git
git clone https://github.com/guelfoweb/knock.git
git clone https://github.com/nahamsec/lazyrecon.git
cd lazyrecon
sudo pip install -r requirements.txt
cd ..
git clone https://github.com/craigz28/firmwalker.git
git clone https://github.com/aboul3la/Sublist3r.git
git clone https://github.com/nahamsec/recon_profile.git
git clone https://github.com/JonathanSalwan/ROPgadget
cd ROPgadget
python setup.py install
apt-get install -y wireshark
cd ~
mkdir tools
cd ~/tools/
wget https://github.com/greatscottgadgets/libbtbb/archive/2018-08-R1.tar.gz -O libbtbb-2018-08-R1.tar.gz
tar -xf libbtbb-2018-08-R1.tar.gz
cd libbtbb-2018-08-R1
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
