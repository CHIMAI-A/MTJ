from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPixmap
import serial.tools.list_ports
import sys
import cv2
import numpy as np
import rpc  # Assuming you have the rpc module installed
from datetime import datetime

class ImgLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        self.status = 'CLICKED'
        self.pos_1st = ev.position()
        self.clicked.emit()
        return super().mousePressEvent(ev)
    
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.status = 'RELEASED'
        self.pos_2nd = ev.position()
        self.clicked.emit()
        return super().mouseReleaseEvent(ev)

class EspCamWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ser_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.populate_ui()
        self.serial_connection = None  # Placeholder for the serial connection
        self.classifier = None

    def populate_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.populate_ui_image()
        self.populate_ui_ctrl()
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.ctrl_layout)

    def populate_ui_image(self):
        self.image_layout = QtWidgets.QVBoxLayout()
        self.image_layout.setAlignment(QtCore.Qt.AlignTop)
        self.preview_img = ImgLabel("Preview Image")
        self.preview_img.resize(320, 240)
        self.image_layout.addWidget(self.preview_img)

    def populate_ui_ctrl(self):
        self.ctrl_layout = QtWidgets.QFormLayout() 
        self.ctrl_layout.setAlignment(QtCore.Qt.AlignTop)
        
        self.esp32_port = QtWidgets.QComboBox()
        self.esp32_port.addItems(self.ser_ports)
        self.ctrl_layout.addRow("ESP32 Port", self.esp32_port)

        self.esp32_button = QtWidgets.QPushButton("Connect")
        self.esp32_button.clicked.connect(self.connect_esp32)
        self.ctrl_layout.addRow(self.esp32_button)

    def connect_esp32(self):
        port = self.esp32_port.currentText()
        self.serial_connection = serial.Serial(port, baudrate=115200, timeout=1)
        self.esp32_button.setText("Grab")
        self.esp32_button.clicked.disconnect()
        self.esp32_button.clicked.connect(self.start_stream)
        self.esp32_button.repaint()

    def start_stream(self):
        while True:
            line = self.serial_connection.readline().decode().strip()
            if line.startswith('Classification:'):
                classification = line.split(':', 1)[1].strip()
                self.update_classification(classification)
            elif line.startswith('Image:'):
                image_data = line.split(':', 1)[1].strip()
                image = np.fromstring(image_data, dtype=np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                self.update_image(image)

    def update_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        img = QtGui.QImage(img.data, w, h, QtGui.QImage.Format_RGB888)
        self.preview_img.setPixmap(QPixmap(img))

    def update_classification(self, classification):
        self.esp32_button.setText(classification)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = EspCamWidget()
    widget.resize(640, 480)
    widget.show()
    sys.exit(app.exec())
