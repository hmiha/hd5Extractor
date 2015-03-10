#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import sys, os
from hd5Extractor import *

class Widget(QtGui.QWidget):
    def __init__(self):
        super(Widget, self).__init__()

        self.openButton = QtGui.QPushButton("Open")
        self.openButton.clicked.connect(self.open_FileDialog)

        self.pathline = QtGui.QLineEdit("")

        self.exeButton = QtGui.QPushButton("Extract")
        self.exeButton.clicked.connect(self.execute)

        self.label = QtGui.QLabel(self)
        self.label.setText('')

        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(self.openButton, 0, 0)
        gridLayout.addWidget(self.pathline, 0, 1)
        gridLayout.addWidget(self.exeButton, 1, 0)
        gridLayout.addWidget(self.label, 1, 1)
        self.setLayout(gridLayout)

        self.setWindowTitle(".h5 Extractor")

        self.resize(400, 40)
        self.move(800, 400)

    def open_FileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~'))
        self.pathline.setText(filename)

    def execute(self):
        # e.g. in case of fpath = 'foo/bar/data.h5'
        fpath = str(self.pathline.text())
        if fpath == '':
            self.label.setText('Set the file path')
            return
        fileDir = os.path.dirname(fpath)    # return 'foo/bar'
        saveDirName = os.path.splitext(os.path.basename(fpath))[0]  # return 'data'
        saveDir = os.path.join(fileDir, saveDirName)    # return 'foo/bar/data/'
        if os.path.exists(saveDir):
            self.label.setText(saveDir + ' already exists.')
            return
        else:
            os.mkdir(saveDir)

        self.label.setText('Now extracting...')
        h5file = load_h5(fpath)
        item_list = [h5file.items()[i][0] for i in xrange(len(h5file.items()))]
        for item in item_list:
            os.mkdir(os.path.join(saveDir, item))
            data = h5file[item].value   # Access to the GROUP using .value method
            n1, n2 = data.shape[ : 2]
            n = n1 * n2
            for i in xrange(n):
                status = read_and_save(item, data, saveDir, i, n1)

        textIO(saveDir)
        self.label.setText('Extracting finished.')
        return

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec_())
