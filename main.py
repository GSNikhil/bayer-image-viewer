import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QFormLayout, QRadioButton, QLineEdit, \
    QLabel, QButtonGroup, QHBoxLayout, QGridLayout, QListWidget, QSizePolicy, QScrollArea, QPushButton, QFileDialog, \
    QSlider
from PyQt5.QtGui import QImage, QPixmap, QPalette, QIntValidator, QIcon
from PyQt5 import QtCore
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAW Image Viewer")
        self.setWindowIcon(QIcon("bayer.png"))

        self.mainWidget = QWidget()
        self._create_left_widget()
        self._create_right_widget()

        grid = QGridLayout()
        grid.addWidget(self.leftWindow, 0, 0, 1, 2)
        grid.addWidget(self.rightWindow, 0, 2, 1, 10)

        self.mainWidget.setLayout(grid)
        self.setCentralWidget(self.mainWidget)

        # Extra / Utility
        self.previtem = None
        self.curritem = None
        self.image = None
        self.shift = 0
        self.width = 0
        self.height = 0
        self.zoom = 1
        self.zoom_label.setText(repr(self.zoom) + "x")

        # Testing Stuff
        self.test()

    def test(self):
        fileName = "C:\\Users\\Hp\\Downloads\\img.jpg"
        image = QImage(fileName)

        self.imageLabel.setPixmap(QPixmap.fromImage(image))

        self.scrollArea.setVisible(True)
        self.imageLabel.adjustSize()

        self.dir.setText("F:/bayer_viewer/sample/")
        self.imgwidth.setText("16")
        self.imgheight.setText("12")
        self.bittage.setText("10")
        self.n_bytes.setText("2")

    def _create_right_widget(self):
        self.rightWindow = QWidget()

        vbox = QVBoxLayout()

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        # btn = QPushButton("Hello!")

        vbox.addWidget(self.scrollArea)
        # vbox.addWidget(btn)

        self.rightWindow.setLayout(vbox)

    def _create_left_widget(self):
        self.leftWindow = QWidget()
        vbox = QVBoxLayout()

        # 0
        self.dir_btn = QPushButton("Select Dir")
        self.dir_btn.clicked.connect(self.getDir)

        # 1
        form = QFormLayout()
        self.dir = QLineEdit()
        form.addRow("Dir: ", self.dir)
        self.imgwidth = QLineEdit()
        self.imgwidth.setValidator(QIntValidator())
        form.addRow("Width: ", self.imgwidth)
        self.imgheight = QLineEdit()
        self.imgheight.setValidator(QIntValidator())
        form.addRow("Height: ", self.imgheight)

        hbox_inline = QHBoxLayout()
        self.bittage = QLineEdit()
        self.bittage.setValidator(QIntValidator())
        self.n_bytes = QLineEdit()
        self.n_bytes.setValidator(QIntValidator())
        form.addRow("Bittage: ", self.bittage)
        form.addWidget(QLabel("in"))
        form.addRow("Bytes: ", self.n_bytes)

        self.zoom_slider = QSlider(QtCore.Qt.Orientation(QtCore.Qt.Horizontal))
        self.zoom_slider.setRange(-20, 20)
        self.zoom_slider.setTickPosition(QSlider.TicksBothSides)
        self.zoom_slider.setTickInterval(5)
        self.zoom_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoom_slider.sliderReleased.connect(lambda: self.setZoom())

        form.addRow("Zoom: ", self.zoom_slider)
        self.zoom_label = QLabel()
        form.addRow("", self.zoom_label)

        # 2
        gainbox = QVBoxLayout()
        gainbox.addWidget(QLabel("Gain"))

        btnGroup = QButtonGroup()

        hbox = QHBoxLayout()
        rbtn1 = QRadioButton("x1")
        rbtn2 = QRadioButton("x2")
        rbtn4 = QRadioButton("x4")
        rbtn8 = QRadioButton("x8")
        rbtn16 = QRadioButton("x16")

        rbtn1.toggled.connect(lambda: self.setShift(0))
        rbtn2.toggled.connect(lambda: self.setShift(1))
        rbtn4.toggled.connect(lambda: self.setShift(2))
        rbtn8.toggled.connect(lambda: self.setShift(3))
        rbtn16.toggled.connect(lambda: self.setShift(4))

        btnGroup.addButton(rbtn1)
        btnGroup.addButton(rbtn2)
        btnGroup.addButton(rbtn4)
        btnGroup.addButton(rbtn8)
        btnGroup.addButton(rbtn16)

        hbox.addWidget(rbtn1)
        hbox.addWidget(rbtn2)
        hbox.addWidget(rbtn4)
        hbox.addWidget(rbtn8)
        hbox.addWidget(rbtn16)

        # 3
        self.searchBtn = QPushButton("Search!")
        self.searchBtn.clicked.connect(self.search)

        # 4
        self.statusLabel = QLabel()

        # 5
        self.list = QListWidget()
        self.list.clicked.connect(self.itemClicked)

        # Done
        vbox.addWidget(self.dir_btn)
        vbox.addLayout(form)
        vbox.addLayout(gainbox)
        vbox.addLayout(hbox)
        # vbox.addWidget(self.zoom_slider)
        vbox.addWidget(self.searchBtn)
        vbox.addWidget(self.statusLabel)
        vbox.addWidget(self.list)

        self.leftWindow.setLayout(vbox)

    def setZoom(self):
        self.zoom = int(self.zoom_slider.value())
        self.zoom = self.zoom - (self.zoom % 5) + 1
        self.zoom_slider.setValue(self.zoom)
        print(self.zoom)

        if self.zoom == -4:
            self.zoom = 0.8
        elif self.zoom == -9:
            self.zoom = 0.6
        elif self.zoom == -14:
            self.zoom = 0.4
        elif self.zoom == -19:
            self.zoom = 0.2

        self.zoom_label.setText(repr(self.zoom) + "x")
        self.displayImg()

    def getDir(self):
        temp = QFileDialog.getExistingDirectory(self, "Open a folder", "", QFileDialog.ShowDirsOnly)
        self.dir.setText(temp)

    def setShift(self, s):
        self.shift = s
        self.loadImg()

    def check(self):

        if self.dir.text() == "":
            self.statusLabel.setText("No directory selected.\n")
            return 0

        if self.imgwidth.text() == "":
            self.imgwidth.setText("0")

        if int(self.imgwidth.text()) <= 0:
            self.statusLabel.setText("Width can not be less than zero.")
            return 0

        if self.imgheight.text() == "":
            self.imgheight.setText("0")

        if int(self.imgheight.text()) <= 0:
            self.statusLabel.setText("Height can not be less than zero.")
            return 0

        if self.bittage.text() == "":
            self.bittage.setText("0")

        if int(self.bittage.text()) <= 0 or int(self.bittage.text()) > 16:
            self.statusLabel.setText("Bittage can not be less than zero or greater than 16.")
            return 0

        if self.n_bytes.text() == "":
            self.n_bytes.setText("0")

        if int(self.n_bytes.text()) < 1 or int(self.n_bytes.text()) > 2:
            self.statusLabel.setText("Only 1 and 2 are allowed in 'Bytes' entry.")
            return 0

        if int(self.bittage.text()) > 8 and int(self.n_bytes.text()) == 1:
            self.statusLabel.setText(f"Unable to fit {self.bittage.text()} into 1 byte.")
            return 0

        self.width = int(self.imgwidth.text())
        self.height = int(self.imgheight.text())

        return 1

    def itemClicked(self):
        self.previtem = self.curritem
        self.curritem = self.list.currentItem()

        if self.previtem == self.curritem:
            return

        self.statusLabel.setText(self.curritem.text())
        self.loadImg()
        self.displayImg()

    def loadImg(self):
        if self.curritem is None:
            return

        self.image = np.zeros((self.height, self.width, 3), dtype=np.uint16)

        path = self.dir.text() + "/" + self.curritem.text()
        # print(path)
        dt = np.dtype(np.uint16) if self.n_bytes.text() == "2" else np.dtype(np.uint8)
        bayer = np.fromfile(path, dtype=dt)
        bayer = bayer.reshape((self.height, self.width))

        # Gr
        self.image[0::2, 0::2, 1] = bayer[0::2, 0::2]
        # R
        self.image[0::2, 1::2, 0] = bayer[0::2, 1::2]
        # B
        self.image[1::2, 0::2, 2] = bayer[1::2, 0::2]
        # Gb
        self.image[1::2, 1::2, 1] = bayer[1::2, 1::2]

        # Shift
        self.image = self.image << self.shift

        max = np.max(self.image)

        if max >= 256:
            # Normalize
            min = np.min(self.image)
            range = max - min

            self.image = ((self.image - min) / range) * 255
            self.image = self.image.astype(np.uint8)

        # print(bayer.shape)

    def displayImg(self):
        if self.curritem is None:
            return

        temp = QImage(self.image.data, self.width, self.height, 3 * self.width, QImage.Format_RGB888)
        print(self.width * self.zoom, self.height * self.zoom)
        temp = temp.scaled(int(self.width * self.zoom), int(self.height * self.zoom))
        temp = QPixmap.fromImage(temp)
        self.imageLabel.setPixmap(temp)
        self.scrollArea.setVisible(True)
        self.imageLabel.adjustSize()

    def search(self):
        if self.check() == 0:
            return

        print(self.dir.text(), self.imgwidth.text(), self.imgheight.text(), self.bittage.text(), self.n_bytes.text())
        bittage = int(self.bittage.text())

        n_pixels = self.height * self.width
        n_byte = int(self.n_bytes.text())
        file_size = n_pixels * n_byte
        count = 0

        self.list.clear()

        dir_list = os.listdir(self.dir.text())
        for item in dir_list:
            if item.endswith(".raw"):
                stat = os.stat(self.dir.text() + "/" + item).st_size
                if stat == file_size:
                    self.list.addItem(item)
                    count += 1

        self.statusLabel.setText(f"{count} items are found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
