import sys
import vtk
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
 
class MainWindow(QMainWindow):
 
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setWindowTitle("vtk_gui")
        self.vl = QGridLayout()
        self.frame = QFrame()
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)

        # vtk setting
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget, 0, 0, 1, 3)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.ren.AddActor(self.actor)
        self.ren.ResetCamera()

        self.m_bShowActor = True

        self.show()
        self.iren.Initialize()

        # button
        self.bt_sphere = QPushButton("Sphere")
        self.vl.addWidget(self.bt_sphere, 1, 0)
        self.bt_sphere.clicked.connect(self.bt_sphere_clicked)

        self.bt_cone = QPushButton("Cone")
        self.vl.addWidget(self.bt_cone, 1, 1)
        self.bt_cone.clicked.connect(self.bt_cone_clicked)

        self.showremove = QPushButton("Show/Remove")
        self.vl.addWidget(self.showremove, 1, 2)
        self.showremove.clicked.connect(self.bt_show_remove)

    def bt_sphere_clicked(self):
        self.source("sphere")

    def bt_cone_clicked(self):
        self.source("cone")

    def bt_show_remove(self):
        if self.m_bShowActor:    
            self.ren.RemoveActor(self.actor)
            self.m_bShowActor = False
        else:
            self.ren.AddActor(self.actor)
            self.m_bShowActor = True

        self.redraw()
    
    def redraw(self):
        self.ren.GetRenderWindow().Render()


    def source(self, flag):
        if flag == "sphere":
            source = vtk.vtkSphereSource()
            source.SetCenter(0, 0, 0)
            source.SetRadius(5.0)
            self.afterSource(source)
        elif flag == "cone":
            source = vtk.vtkConeSource()
            self.afterSource(source)


    def afterSource(self, source):
            self.mapper.SetInputConnection(source.GetOutputPort())
            self.ren.ResetCamera()
            self.iren.Initialize()

   

        
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
