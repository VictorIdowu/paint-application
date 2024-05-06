from PyQt6.QtWidgets import QMainWindow,QApplication,QLabel,QStatusBar,QToolBar,QColorDialog,QFileDialog
from PyQt6.QtGui import QPaintEvent, QPixmap,QPainter,QPen,QColor,QAction,QIcon
from PyQt6.QtCore import Qt,QPoint,QRect,QSize
import sys
import os

class Canvas(QLabel):
  def __init__(self,parent=None):
    super().__init__(parent)
    self.parent = parent
    self.initUI()

  def initUI(self):
    self.pixmap = QPixmap(600,600)
    self.pixmap.fill(Qt.GlobalColor.white)
    self.setPixmap(self.pixmap)
    self.setMouseTracking(True)
    self.drawing = False
    self.last_mouse_pos = QPoint()
    self.status_label = QLabel()

    self.eraser = False
    self.pen_color = Qt.GlobalColor.black
    self.pen_width = 1

  def mouseMoveEvent(self,event):
    mouse_position = event.pos()
    status_text = f"Mouse cordinates are: {mouse_position.x(),mouse_position.y()}"
    self.status_label.setText(status_text)
    self.parent.statusBar.addWidget(self.status_label)
    if (event.buttons() and Qt.MouseButton.LeftButton) and self.drawing:
      # Draw Something
      self.draw(mouse_position)

  def mousePressEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      self.last_mouse_pos = event.pos()
      self.drawing = True
      # print(f"Left click at position: {str(event.pos())}")
      

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.MouseButton.LeftButton:
      self.drawing = False
      # print(f"Mouse released at position: {str(event.pos())}")

  def draw(self, points):
    painter = QPainter(self.pixmap)
    if self.eraser == False:
      pen = QPen(self.pen_color,self.pen_width)

      painter.setPen(pen)
      painter.drawLine(self.last_mouse_pos,points)
      self.last_mouse_pos = points
    elif self.eraser == True:
      eraser = QRect(points.x(),points.y(),12,12)
      painter.eraseRect(eraser)
    
    self.update()
  
  def paintEvent(self, event):
    painter = QPainter(self)
    target_rect = QRect()
    target_rect = event.rect()
    painter.drawPixmap(target_rect, self.pixmap,target_rect)
  
  def selectTool(self,tool):
    if tool == "pencil":
      self.pen_width = 2
      self.eraser = False
    elif tool == "marker":
      self.pen_width = 4
      self.eraser = False
    elif tool == "eraser":
      self.eraser = True
    elif tool == "color":
      self.eraser = False
      color = QColorDialog.getColor()
      self.pen_color = color
  
  def new(self):
    self.pixmap.fill(Qt.GlobalColor.white)
    self.update()
  
  def save_file(self):
    file_name,_ = QFileDialog.getSaveFileName(self, "Save As", os.path.curdir+"sample.png", "PNG File(*.png)")
    if file_name:
      self.pixmap.save(file_name, "png")

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    self.setMinimumSize(600,600)
    self.setWindowTitle("Paint App")

    # Create canvas
    canvas = Canvas(self)
    self.setCentralWidget(canvas)
    self.statusBar = QStatusBar()
    self.setStatusBar(self.statusBar)

    # Adding toolbar
    tool_bar = QToolBar("Toolbar")
    tool_bar.setIconSize(QSize(24,24))
    self.addToolBar(Qt.ToolBarArea.TopToolBarArea, tool_bar)
    tool_bar.setMovable(False)

    pencil_act = QAction(QIcon("icons/pencil.png"), "Pencil", tool_bar)
    marker_act = QAction(QIcon("icons/marker.png"), "Marker", tool_bar)
    eraser_act = QAction(QIcon("icons/eraser.png"), "Eraser", tool_bar)
    colors_act = QAction(QIcon("icons/colors.png"), "Colors", tool_bar)

    pencil_act.triggered.connect(lambda : canvas.selectTool("pencil"))
    marker_act.triggered.connect(lambda : canvas.selectTool("marker"))
    eraser_act.triggered.connect(lambda : canvas.selectTool("eraser"))
    colors_act.triggered.connect(lambda : canvas.selectTool("color"))

    tool_bar.addAction(pencil_act) 
    tool_bar.addAction(marker_act) 
    tool_bar.addAction(eraser_act) 
    tool_bar.addAction(colors_act) 

    # Menu bar
    self.new_act = QAction("New")
    self.new_act.triggered.connect(canvas.new)

    self.save_file_act = QAction("Save")
    self.save_file_act.triggered.connect(canvas.save_file)

    self.quit_act = QAction("Exit")
    self.quit_act.triggered.connect(self.close)

    self.menuBar().setNativeMenuBar(False)

    file_menu = self.menuBar().addMenu("File")
    file_menu.addAction(self.new_act)
    file_menu.addAction(self.save_file_act)
    file_menu.addSeparator()
    file_menu.addAction(self.quit_act)



app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()