# TUG
A PyQt5 interface for Tinfoil (usb_install_pc.py)
https://github.com/Adubbz/Tinfoil

## Download
Full releases are located at:
https://github.com/nxmango/tug/releases/latest

## Windows Instructions:
1. Download & Install Python 3 from https://www.python.org/downloads/
2. Download Zadig from https://zadig.akeo.ie/.
3. With your Switch plugged in and on the Tinfoil USB install menu,
   choose "List All Devices" under the options menu in Zadig, and select libnx USB comms.
4. Choose libusbK from the driver list and click the "Replace Driver" button.
5. Go to Tinfoil > Title Management > USB Install NSP
6. Double-click on tug.pyw

## macOS Instructions:
1. Install Homebrew from https://brew.sh
2. Install Python 3 from https://www.python.org/downloads/
      * sudo mkdir /usr/local/Frameworks
      * sudo chown $(whoami) /usr/local/Frameworks
      * brew install python
3. Install PyUSB
      * pip3 install pyusb
4. Install libusb
      * brew install libusb
5. Plug in your Switch and go to Tinfoil > Title Management > USB Install NSP
6. Double-click on tug.pyw
