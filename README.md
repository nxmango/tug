# TUG
A PyQt5 interface for Tinfoil (usb_install_pc.py)
https://github.com/Adubbz/Tinfoil

## Download
Full releases are located at:
https://github.com/nxmango/tug/releases/latest

## Windows Instructions:
1. Download Zadig from https://zadig.akeo.ie/.
2. With your Switch plugged in and on the Tinfoil USB install menu,
   choose "List All Devices" under the options menu in Zadig, and select libnx USB comms.
3. Choose libusbK from the driver list and click the "Replace Driver" button.
4. Go to Tinfoil > Title Management > USB Install NSP
5. Double-click on tug.pyw

## macOS Instructions:
1. Install Homebrew https://brew.sh
2. Install Python 3
      sudo mkdir /usr/local/Frameworks
      sudo chown $(whoami) /usr/local/Frameworks
      brew install python
3. Install PyUSB
      pip3 install pyusb
4. Install libusb
      brew install libusb
5. Plug in your Switch and go to Tinfoil > Title Management > USB Install NSP
6. Double-click on tug.pyw
