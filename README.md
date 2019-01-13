# TUG
A PyQt5 interface for Tinfoil (usb_install_pc.py)
https://github.com/Adubbz/Tinfoil

## Download
Full releases are located at:
https://github.com/nxmango/tug/releases/latest

## Windows Instructions:
1. Download & Install Python 3 from https://www.python.org/downloads/
2. Install PyQt5
      * pip install pyqt5
3. Download Zadig from https://zadig.akeo.ie/.
4. With your Switch plugged in and on the Tinfoil USB install menu,
   choose "List All Devices" under the options menu in Zadig, and select libnx USB comms.
5. Choose libusbK from the driver list and click the "Replace Driver" button.
6. Go to Tinfoil > Title Management > USB Install NSP
7. Double-click on tug.pyw

## macOS Instructions:
1. Install Homebrew from https://brew.sh
2. Install Python 3 from https://www.python.org/downloads/
      * sudo mkdir /usr/local/Frameworks
      * sudo chown $(whoami) /usr/local/Frameworks
      * brew install python
3. Install PyQt5
      * pip3 install pyqt5
4. Install PyUSB
      * pip3 install pyusb
5. Install libusb
      * brew install libusb
6. Plug in your Switch and go to Tinfoil > Title Management > USB Install NSP
7. Double-click on tug.pyw
