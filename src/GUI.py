"""
MIT License

Copyright (c) 2020 K Sai Vishwak

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

"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util import numpy_support

# Custom widget imports for DICOM and VTK visualization
from Dicom_Widget import *
from VTK_Widget import *
import Title_Bar


class Mainwindow(QMainWindow):
	"""Main Window Class for the DICOM Viewer"""
	def __init__(self, parent = None):
		super().__init__()
		self.HEIGHT = 600
		self.WIDTH = 900
		self.PATH = ""
		self.setWindowTitle('INFINITT Dicom Viewer')
		self.InitUi()

	def InitUi(self):
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.resize(self.WIDTH, self.HEIGHT)
		self.Grid_Layout = QGridLayout()
		self.Grid_Layout.setObjectName('Grid_Layout')
		self.Grid_Layout.setColumnStretch(0, 1)  #sets the first column (column 0) to have a stretch factor of 1
		self.Grid_Layout.setColumnStretch(1, 4)  #sets the second column (column 1) to have a stretch factor of 3
		self.Grid_Layout.setColumnStretch(2, 4)
		self.Grid_Layout.setColumnStretch(3, 1)
		self.frame = QFrame()
		self.frame.setObjectName('frame')


		
		# --------------- Dicom_Widget -----------
		self.Dicom_Layout = QVBoxLayout()
  		# Dicom_Widget instances for Axial, Sagittal, and Coronal views
	
		# Axial Viewer Layout
		self.axialLayout = QVBoxLayout()
		self.axialSlider = QSlider(Qt.Horizontal)
		self.Axial_Widget = Dicom_Widget(self, "Axial")
		self.Axial_Widget.photoClicked.connect(self.photoClicked_A)
		self.axialLayout.addWidget(self.axialSlider)  # Add the slider to the layout first
		self.axialLayout.addWidget(self.Axial_Widget)  # Then add the viewer widget
		
		# Similar setup for Sagittal and Coronal viewers
		self.sagittalLayout = QVBoxLayout()
		self.sagittalSlider = QSlider(Qt.Horizontal)
		self.Sagittal_Widget = Dicom_Widget(self, "Sagittal")
		self.Sagittal_Widget.photoClicked.connect(self.photoClicked_S)
		self.sagittalLayout.addWidget(self.sagittalSlider)
		self.sagittalLayout.addWidget(self.Sagittal_Widget)

		self.coronalLayout = QVBoxLayout()
		self.coronalSlider = QSlider(Qt.Horizontal)
		self.Coronal_Widget = Dicom_Widget(self, "Coronal")
		self.Coronal_Widget.photoClicked.connect(self.photoClicked_C)
		self.coronalLayout.addWidget(self.coronalSlider)
		self.coronalLayout.addWidget(self.Coronal_Widget)

		# Initialize the labels for displaying the slice numbers
		self.Axial_Slice = QLabel("Axial Slice")
		self.Sagittal_Slice = QLabel("Sagittal Slice")
		self.Coronal_Slice = QLabel("Coronal Slice")

		# Add them to their respective layouts
		self.axialLayout.addWidget(self.Axial_Slice)
		self.sagittalLayout.addWidget(self.Sagittal_Slice)
		self.coronalLayout.addWidget(self.Coronal_Slice)

		# Connecting sliders to update image index and label text
		self.axialSlider.valueChanged.connect(lambda value: [self.Axial_Widget.update_image_index(value), self.updateSliceLabels()])
		self.sagittalSlider.valueChanged.connect(lambda value: [self.Sagittal_Widget.update_image_index(value), self.updateSliceLabels()])
		self.coronalSlider.valueChanged.connect(lambda value: [self.Coronal_Widget.update_image_index(value), self.updateSliceLabels()])


		self.Axial_Widget.setMinimumHeight(150)  # Example height, adjust as needed
		self.Sagittal_Widget.setMinimumHeight(150)
		self.Coronal_Widget.setMinimumHeight(150)
		# self.Axial_Widget.setMaximumWidth(150)  # Example width, adjust as needed
		# self.Sagittal_Widget.setMaximumWidth(150)
		# self.Coronal_Widget.setMaximumWidth(150)


		self.Dicom_Layout.addLayout(self.axialLayout)
		self.Dicom_Layout.addLayout(self.sagittalLayout)
		self.Dicom_Layout.addLayout(self.coronalLayout)





		# ---------------- VTK Widget --------------
		self.vtk = VTK_Widget(self)
		self.vtk.setObjectName('VTK_Widget')
		self.seg_data = []
		self.ArrayDicom = []
		self.thresh_val = 300
		

		# ----------------- Dicom Tools Layout ------
		self.Dicom_Tool_Layout = QVBoxLayout()
		self.Dicom_Tool_Layout.setObjectName('Dicom_Tool_Layout')
		self.Dicom_Tool_Layout.setSpacing(15)


		self.Import_Button = QToolButton(self)
		self.Import_Button.setToolTip('Import Dicom...')
		if os.sep=='\\':
			self.Import_Button.setIcon(QIcon('..\\Images\\file_import.png'))
		else:
			self.Import_Button.setIcon(QIcon('../Images/file_import.png'))
		self.Import_Button.setIconSize(QtCore.QSize(25, 25))
		self.Import_Button.clicked.connect(self.get_dir)

		self.Segment_Button = QToolButton(self)
		self.Segment_Button.setToolTip('Segment Bone')
		if os.sep=='\\':
			self.Segment_Button.setIcon(QIcon('..\\Images\\segment.png'))
		else:
			self.Segment_Button.setIcon(QIcon('../Images/segment.png'))
		self.Segment_Button.setIconSize(QtCore.QSize(25, 25))
		self.Segment_Button.clicked.connect(self.Segment_Bone)

		self.Show_Segment_Button = QToolButton(self)
		self.Show_Segment_Button.setToolTip('Show Segmentation')
		if os.sep=='\\':
			self.Show_Segment_Button.setIcon(QIcon('..\\Images\\show_segment.png'))
		else:
			self.Show_Segment_Button.setIcon(QIcon('../Images/show_segment.png'))
		self.Show_Segment_Button.setIconSize(QtCore.QSize(25, 25))
		self.Show_Segment_Button.clicked.connect(self.Hide_Segment)

		self.Render_Button = QToolButton(self)
		self.Render_Button.setToolTip('Show 3D')
		if os.sep=='\\':
			self.Render_Button.setIcon(QIcon('..\\Images\\render.png'))
		else:
			self.Render_Button.setIcon(QIcon('../Images/render.png'))
		self.Render_Button.setIconSize(QtCore.QSize(25, 25))
		self.Render_Button.clicked.connect(self.Show_Render)

		self.Export_Button = QToolButton(self)
		self.Export_Button.setToolTip('Export STL')
		if os.sep=='\\':
			self.Export_Button.setIcon(QIcon('..\\Images\\surface_export.png'))
		else:
			self.Export_Button.setIcon(QIcon('../Images/surface_export.png'))
		self.Export_Button.setIconSize(QtCore.QSize(25, 25))
		self.Export_Button.clicked.connect(self.Export_Stl)

		self.Axial_Full = QToolButton(self)
		self.Axial_Full.setObjectName("Axial_Full")
		self.Axial_Full.setToolTip('Axial Full Screen')
		if os.sep=='\\':
			self.Axial_Full.setIcon(QIcon('..\\Images\\axial_full.png'))
		else:
			self.Axial_Full.setIcon(QIcon('../Images/axial_full.png'))
		self.Axial_Full.setIconSize(QtCore.QSize(25, 25))
		self.Axial_Full.clicked.connect(self.Full_Screen)

		self.Sagittal_Full = QToolButton(self)
		self.Sagittal_Full.setObjectName("Sagittal_Full")
		self.Sagittal_Full.setToolTip('Sagittal Full Screen')
		if os.sep=='\\':
			self.Sagittal_Full.setIcon(QIcon('..\\Images\\sagittal_full.png'))
		else:
			self.Sagittal_Full.setIcon(QIcon('../Images/sagittal_full.png'))
		self.Sagittal_Full.setIconSize(QtCore.QSize(25, 25))
		self.Sagittal_Full.clicked.connect(self.Full_Screen)

		self.Coronal_Full = QToolButton(self)
		self.Coronal_Full.setObjectName("Coronal_Full")
		self.Coronal_Full.setToolTip('Coronal Full Screen')
		if os.sep=='\\':
			self.Coronal_Full.setIcon(QIcon('..\\Images\\coronal_full.png'))
		else:
			self.Coronal_Full.setIcon(QIcon('../Images/coronal_full.png'))
		self.Coronal_Full.setIconSize(QtCore.QSize(25, 25))
		self.Coronal_Full.clicked.connect(self.Full_Screen)

		self._3D_Full = QToolButton(self)
		self._3D_Full.setObjectName("_3D_Full")
		self._3D_Full.setToolTip('3D Full Screen')
		if os.sep=='\\':
			self._3D_Full.setIcon(QIcon('..\\Images\\3d_full.png'))
		else:
			self._3D_Full.setIcon(QIcon('../Images//3d_full.png'))
		self._3D_Full.setIconSize(QtCore.QSize(25, 25))
		self._3D_Full.clicked.connect(self.Full_Screen)

		self.Dicom_Tool_Layout.addWidget(self.Import_Button)
		self.Dicom_Tool_Layout.addWidget(self.Segment_Button)
		self.Dicom_Tool_Layout.addWidget(self.Show_Segment_Button)
		self.Dicom_Tool_Layout.addWidget(self.Render_Button)
		self.Dicom_Tool_Layout.addWidget(self.Export_Button)
		#self.Dicom_Tool_Layout.addWidget(self.Axial_Full)
		#self.Dicom_Tool_Layout.addWidget(self.Sagittal_Full)
		#self.Dicom_Tool_Layout.addWidget(self.Coronal_Full)
		#self.Dicom_Tool_Layout.addWidget(self._3D_Full)
		verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.Dicom_Tool_Layout.addItem(verticalSpacer)

		# ------------------ VTK Tools Layout -------
		self.VTK_Tool_Layout = QVBoxLayout()
		self.VTK_Tool_Layout.setObjectName('VTK_Tool_Layout')
		self.VTK_Tool_Layout.setSpacing(15)

		Window_Color = QToolButton(self)
		Window_Color.setToolTip('Set 3D window color')
		if os.sep=='\\':
			Window_Color.setIcon(QIcon('..\\Images\\window_color.png'))
		else:
			Window_Color.setIcon(QIcon('../Images/window_color.png'))
		Window_Color.setIconSize(QtCore.QSize(25, 25))
		Window_Color.clicked.connect(self.change_render_color)

		Actor_Color = QToolButton(self)
		Actor_Color.setToolTip('Set 3D body color')
		if os.sep=='\\':
			Actor_Color.setIcon(QIcon('..\\Images\\actor_color.png'))
		else:
			Actor_Color.setIcon(QIcon('../Images/actor_color.png'))
		Actor_Color.setIconSize(QtCore.QSize(25, 25))
		Actor_Color.clicked.connect(self.change_actor_color)

		self.VTK_Tool_Layout.addWidget(Window_Color)
		self.VTK_Tool_Layout.addWidget(Actor_Color)
		self.VTK_Tool_Layout.addItem(verticalSpacer)

		
		# ------------------- Title Bar --------------
		self.TitleBar= Title_Bar.TitleBar(self)
		self.TitleBar.setObjectName('TitleBar')

		# -------------------- Status Widget ----------
		self.Dir_Status = QLabel(self)
		self.Dir_Status.setObjectName('Dir_Status')

		# ---------------- Final Layout ---------------
		self.Grid_Layout.addWidget(self.TitleBar, 0, 0, 1, 4)
		self.Grid_Layout.addLayout(self.Dicom_Tool_Layout, 1, 0, 1, 1)
		self.Grid_Layout.addLayout(self.Dicom_Layout, 1, 1, 1, 1)
		self.Grid_Layout.addWidget(self.vtk, 1, 2, 1, 1)
		self.Grid_Layout.addLayout(self.VTK_Tool_Layout, 1, 3, 1, 1)
		self.Grid_Layout.addWidget(self.Dir_Status, 2, 0, 1, 4)


		self.frame.setLayout(self.Grid_Layout)
		self.setContentsMargins(0, 0, 0, 0)
		self.setCentralWidget(self.frame)
		self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)

		self.show()

	def Full_Screen(self):
		pass

	def Export_Stl(self):
		if self.vtk.vti_write:			
			try:
				name = QFileDialog.getSaveFileName(self, 'Save File')
				file = open(name[0],'w')
				file.write("")
				file.close()
				try:
					self.vtk.export_stl(format(name[0]))
					print('File Saved\n')
				except:
					print('Unable to Save\n')
			except:
				print("Canceled\n")
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Please Segment Data')
			msg.setWindowTitle("Error")
			msg.exec_()

	def Show_Render(self):
		if self.vtk.vti_write:
			print('Rendering..........\n')
			self.vtk.show_render()
		else:
			print('Segment First....\n')
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('No Data to render')
			msg.setWindowTitle("Error")
			msg.exec_()

	def Hide_Segment(self):
		if len(self.seg_data) == 0 or len(self.ArrayDicom) == 0:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Please Segment Data')
			msg.setWindowTitle("Error")
			msg.exec_()
			return
		self.Axial_Widget.hide_segmentation()
		self.Sagittal_Widget.hide_segmentation()
		self.Coronal_Widget.hide_segmentation()


	def Segment_Bone(self):
		if len(self.ArrayDicom) == 0:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('Please Load Dicom')
			msg.setWindowTitle("Error")
			msg.exec_()
			return
		print('Segmenting Bone..... \n')
		self.seg_data = self.ArrayDicom.copy()
		self.seg_data[self.seg_data < self.thresh_val] = 0
		self.seg_data[self.seg_data >= self.thresh_val] = 255

		self.Axial_Widget.seg_data = self.seg_data
		self.Sagittal_Widget.seg_data = self.seg_data
		self.Coronal_Widget.seg_data = self.seg_data
		self.Axial_Widget.update_image()
		self.Sagittal_Widget.update_image()
		self.Coronal_Widget.update_image()
		print('Writing VTI..........\n')
		self.vtk.write_vti(self.seg_data, self.ConstPixelSpacing, filename = 'Polydata.vti', origin = (0, 0, 0))

	def photoClicked_A(self, pos):
		self.Axial_Slice.setText('%d' % (pos.x()))

	def photoClicked_S(self, pos):
		self.Sagittal_Slice.setText('%d' % (pos.x()))

	def photoClicked_C(self, pos):
		self.Coronal_Slice.setText('%d' % (pos.x()))

	def get_dir(self):
		try:
			filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
			if filename:
				if os.sep=='\\':
					filename=filename.replace('/', "\\")
			self.PATH = filename
			print('Dicom Imported from', self.PATH, "\n")
		except:
			print('Failed Loading')

		if filename != "":
			self.reader = vtk.vtkDICOMImageReader()
			self.reader.SetDirectoryName(self.PATH)
			self.reader.Update()

			_extent = self.reader.GetDataExtent()
			self.ConstPixelDims = [_extent[1]-_extent[0]+1, _extent[3]-_extent[2]+1, _extent[5]-_extent[4]+1]
			self.ConstPixelSpacing = self.reader.GetPixelSpacing()
			pointData = self.reader.GetOutput().GetPointData()
			arrayData = pointData.GetArray(0)
			self.ArrayDicom = numpy_support.vtk_to_numpy(arrayData)
			self.ArrayDicom = self.ArrayDicom.reshape(self.ConstPixelDims, order='F')
			print('shape of 3D array', self.ArrayDicom.shape, "\n")
			self.Axial_Widget.ArrayDicom = self.ArrayDicom
			self.Axial_Widget.remove_segmentation()
			self.Axial_Widget.update_image()
			self.Sagittal_Widget.ArrayDicom = self.ArrayDicom
			self.Sagittal_Widget.remove_segmentation()
			self.Sagittal_Widget.update_image()
			self.Coronal_Widget.ArrayDicom = self.ArrayDicom
			self.Coronal_Widget.remove_segmentation()
			self.Coronal_Widget.update_image()
			self.vtk.vti_write == False
			self.Dir_Status.setText(filename)
			self.vtk.clean_gui()
			self.axialSlider.setMaximum(self.ConstPixelDims[2] - 1)  # axial slices are along the Z-axis,parallel to the XY plane
			self.sagittalSlider.setMaximum(self.ConstPixelDims[0] - 1)  # sagittal slices are along the X-axis, parallel to the YZ plane
			self.coronalSlider.setMaximum(self.ConstPixelDims[1] - 1)  # Assuming coronal slices are along the Y-axis, parallel to the XZ plane
			# Update the slice labels for the initial position
			self.updateSliceLabels(0)  # Assuming starting at the first slice for all views


	def updateSliceLabels(self, value=None):  # `value` is optional, only used when called by slider valueChanged
		# Updating the labels with the current slider value + 1 (to display in a user-friendly 1-indexed format)
		self.Axial_Slice.setText(f"Axial Slice: {self.axialSlider.value() + 1}/{self.axialSlider.maximum() + 1}")
		self.Sagittal_Slice.setText(f"Sagittal Slice: {self.sagittalSlider.value() + 1}/{self.sagittalSlider.maximum() + 1}")
		self.Coronal_Slice.setText(f"Coronal Slice: {self.coronalSlider.value() + 1}/{self.coronalSlider.maximum() + 1}")

	def change_render_color(self):
		color = QColorDialog.getColor().getRgb()
		self.vtk.renderer.SetBackground(color[0] / 255, color[1] / 255, color[2] / 255)
		self.vtk.iren.Initialize()
		self.vtk.iren.Start()

	def change_actor_color(self):
		if self.vtk.actor:
			color = QColorDialog.getColor().getRgb()
			self.vtk.actor.GetProperty().SetColor(color[0] / 255, color[1] / 255, color[2] / 255)
			self.vtk.iren.Initialize()
			self.vtk.iren.Start()
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Error")
			msg.setInformativeText('No 3D Data')
			msg.setWindowTitle("Error")
			msg.exec_()

