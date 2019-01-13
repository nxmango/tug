"""""
MIT License

Copyright (c) 2019 nxmango

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""""

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from tkinter import messagebox
from usb_install_pc import send_nsp_list, poll_commands
import tkinter as tk

"""
Exceptions for imports (PyUSB & PyQt5)
from fourminute
"""
root = tk.Tk()
root.withdraw()
try:
    import usb.core
    import usb.util
except ImportError:
    messagebox.showinfo("Error","PyUSB not found. Please install with 'pip3 install pyusb'\nIf you are on macOS, also install LibUSB with 'brew install libusb'.")
    exit()
try:
    from PyQt5 import QtWidgets, QtGui
    from PyQt5.QtWidgets import QFileDialog, QListWidget, QMessageBox
except ImportError:
    messagebox.showinfo("Error","PyQt5 not found. Please install with 'pip3 install pyqt5'.")
    exit()

class TUG(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.b_folder = QtWidgets.QPushButton("Select folder")
        self.b_header = QtWidgets.QPushButton("Send header")
        self.b_header.setEnabled(False)
        self.l_folder = QtWidgets.QLabel("No folder selected")
        self.list_header = QtWidgets.QListWidget()
        self.folder = ""

        # Find Nintendo Switch
        self.dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
        if self.dev is None:
            QMessageBox.warning(self, "Warning", "Nintendo Switch can't be found, try again.")
            exit()
        self.dev.reset()
        self.dev.set_configuration()
        cfg = self.dev.get_active_configuration()
        is_out_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT
        is_in_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN
        self.out_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=is_out_ep)
        self.in_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=is_in_ep)
        assert self.out_ep is not None
        assert self.in_ep is not None

        self.init_ui()

    def init_ui(self):

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.b_folder)
        v_box.addWidget(self.list_header)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.l_folder)
        h_box.addWidget(self.b_header)

        v_box.addLayout(h_box)

        self.setLayout(v_box)
        self.setWindowTitle('TUG')

        self.b_folder.clicked.connect(self.choose_folder)
        self.b_header.clicked.connect(self.send_header)

        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.show()

    def choose_folder(self):
        self.b_header.setEnabled(False)
        self.l_folder.setText("No folder selected")
        self.list_header.clear()
        self.folder = ""
        try:
            self.folder = str(QFileDialog.getExistingDirectory(self, "Select Folder"))
            self.l_folder.setText(self.folder)
            for file in os.listdir(self.folder):
                if file.endswith(".nsp"):
                    self.list_header.addItem(os.path.join(file))
        except:
            self.l_folder.setText("No folder selected")
            pass
        if len(self.folder) > 0:
            self.b_header.setEnabled(True)
            self.folder = Path(self.folder)

    def send_header(self):
        try:
            send_nsp_list(self.folder, self.out_ep)
            poll_commands(self.folder, self.in_ep, self.out_ep)
        except:
            QMessageBox.critical(self, "Critical", "Connection lost to Nintendo Switch, exiting.")
            exit()

app = QtWidgets.QApplication(sys.argv)
ex = TUG()
sys.exit(app.exec_())
