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
import threading
file  = open("config.py", "w")
file.write("cur_prog = 0\nend_prog = 0")
file.close()
import config
from pathlib import Path
from tkinter import messagebox
from usb_install_pc import send_nsp_list, poll_commands
import tkinter as tk
root = tk.Tk()
root.withdraw()

"""
Exceptions for imports (PyUSB & PyQt5)
from fourminute
"""
try:
    import usb.core
    import usb.util
except ImportError:
    messagebox.showinfo("Error","PyUSB not found. Please install with 'pip3 install pyusb'\nIf you are on MacOS, also install LibUSB with 'brew install libusb'.")
    exit()
try:
    from PyQt5.QtCore import Qt, QThread
    from PyQt5 import QtWidgets, QtGui
    from PyQt5.QtWidgets import QFileDialog, QListWidget, QMessageBox, QProgressBar, QApplication
except ImportError:
    messagebox.showinfo("Error","PyQt5 not found. Please install with 'pip3 install pyqt5'.")
    exit()

"""
Seperate thread for installs.
from fourminute
"""
class Install(QThread):
    def __init__(self, nsp_dir, in_ep, out_ep):
        super(Install, self).__init__()
        self.nsp_dir = nsp_dir
        self.in_ep = in_ep
        self.out_ep = out_ep
    def run(self):
        try:
            send_nsp_list(self.nsp_dir, self.out_ep)
            poll_commands(self.nsp_dir, self.in_ep, self.out_ep)
        except Exception as e:
            print(str(e))
            
class TUG(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    """
    Update progress bar.
    from fourminute
    """
    def update_progress(self):
        maxcount = self.list_header.count()
        self.l_folder.setText(str(maxcount) + " NSPs selected.")
        while True: 
            try:
                cur = config.cur_prog
                end = config.end_prog
                v = (cur / end) * 100
                self.progressBar.setValue(v)
                QApplication.processEvents()
            except:
                pass
            
    def init_ui(self):
        self.b_folder = QtWidgets.QPushButton("Select folder")
        self.b_header = QtWidgets.QPushButton("Send header")
        self.b_header.setEnabled(False)
        self.l_folder = QtWidgets.QLabel("No folder selected")
        self.list_header = QtWidgets.QListWidget()
        self.folder = ""
        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignVCenter)
        self.progressBar.setMaximum(100)
        
        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.b_folder)
        v_box.addWidget(self.list_header)
        v_box.addWidget(self.progressBar)

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
            
                
    def send_header(self):
        try:
            nsp_dir = Path(self.folder)
        except:
            pass

        dev = usb.core.find(idVendor=0x057E, idProduct=0x3000)
        if dev is None:
            QMessageBox.warning(self, "Warning", "Couldn't find Nintendo Switch")

        try:
            dev.reset()
            dev.set_configuration()
            cfg = dev.get_active_configuration()

            is_out_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT
            is_in_ep = lambda ep: usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN
            out_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=is_out_ep)
            in_ep = usb.util.find_descriptor(cfg[(0, 0)], custom_match=is_in_ep)

            assert out_ep is not None
            assert in_ep is not None
            
            self.install = Install(nsp_dir, in_ep, out_ep)
            self.install.start()
            self.b_header.setEnabled(False)
            threading.Thread(target = self.update_progress).start()
        except Exception as e:
            print(str(e))

app = QtWidgets.QApplication(sys.argv)
ex = TUG()
sys.exit(app.exec_())
