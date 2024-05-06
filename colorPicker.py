from PyQt6.QtWidgets import QWidget,QApplication,QSlider,QLabel,QHBoxLayout,QVBoxLayout
from PyQt6.QtCore import Qt
import sys

class MainWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setGeometry(0,0,700,500)

    # Sliders
    self.red_slider = QSlider(Qt.Orientation.Horizontal)
    self.green_slider = QSlider(Qt.Orientation.Horizontal)
    self.blue_slider = QSlider(Qt.Orientation.Horizontal)

    for slider in [self.red_slider,self.green_slider,self.blue_slider]:
      slider.setRange(0,255)
      slider.setValue(255)
      slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
      slider.setTickInterval(25)

    # Labels
    self.red_label = QLabel("Red: ")
    self.green_label = QLabel("Green: ")
    self.blue_label = QLabel("Blue: ")
    # value labels
    self.red_value_label = QLabel("255")
    self.green_value_label = QLabel("255")
    self.blue_value_label = QLabel("255")

    # Main Window Layout
    layout = QVBoxLayout(self)

    sliders_layout = QVBoxLayout()

    for label,slider,value_label in zip([self.red_label,self.green_label,self.blue_label],
        [self.red_slider,self.green_slider,self.blue_slider],
        [self.red_value_label,self.green_value_label,self.blue_value_label]
        ):
      slider_layout = QHBoxLayout()
      slider_layout.addWidget(label)
      slider_layout.addWidget(slider)
      slider_layout.addWidget(value_label)
      
      sliders_layout.addLayout(slider_layout)
    
    layout.addLayout(sliders_layout)

    # Connect sliders to a method
    self.red_slider.valueChanged.connect(self.update_color)
    self.green_slider.valueChanged.connect(self.update_color)
    self.blue_slider.valueChanged.connect(self.update_color)

  def update_color(self):
    red = self.red_slider.value()
    green = self.green_slider.value()
    blue = self.blue_slider.value()

    self.red_value_label.setText(str(red))
    self.green_value_label.setText(str(green))
    self.blue_value_label.setText(str(blue))



app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()