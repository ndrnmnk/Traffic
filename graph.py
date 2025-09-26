from PyQt5.QtWidgets import QWidget, QComboBox, QLineEdit, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from backend import *

limits = [1500, 1440, 100, 50, 3600, 100]

class GraphDisplay(QWidget):
	def __init__(self, parent_app):
		super().__init__(parent_app)

		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("Traffic graph")

		self.grid = QGridLayout()

		self.graph_canvas = MplCanvas(width=5, height=4, dpi=100)
		self.grid.addWidget(self.graph_canvas, 0, 0, 5, 4)

		self.x_dd = QComboBox()
		self.y_dd = QComboBox()

		self.x_dd.addItems(["Кількість абонентів", "Довжина робочого дня", "Кількість сеансів зв'язку", "Кількість каналів", "Довжина сеансу зв'язку", "Вірогідність передзвону"])
		self.y_dd.addItems(["Трафік багатоканальної системи", "Трафік системи на канал", "Вірогідність затримки зв'язку Pc", "Вірогідність відмови системи Pb", "Вірогідність відмови системи Pa"])

		self.grid.addWidget(QLabel("X:"), 0, 5)
		self.grid.addWidget(self.x_dd, 1, 5)
		self.grid.addWidget(QLabel("Y:"), 2, 5)
		self.grid.addWidget(self.y_dd, 3, 5)

		self.from_entry = QLineEdit()
		self.to_entry = QLineEdit()

		self.from_entry.setValidator(QIntValidator(1, 1500, self))
		self.to_entry.setValidator(QIntValidator(1, 1500, self))
		self.from_entry.setText("1")
		self.to_entry.setText("100")

		self.grid.addWidget(QLabel("Від"), 5, 0)
		self.grid.addWidget(self.from_entry, 5, 1)
		self.grid.addWidget(QLabel("до"), 5, 2)
		self.grid.addWidget(self.to_entry, 5, 3)

		self.build_btn = QPushButton("Побудувати")
		self.build_btn.pressed.connect(self.on_build)
		self.grid.addWidget(self.build_btn, 5, 5)

		self.setLayout(self.grid)
		self.show()

	def update_graph(self, new_x_list=None, new_y_list=None):
		self.graph_canvas.axes.cla()
		if new_x_list:
			self.graph_canvas.axes.plot(new_x_list, new_y_list)
		self.graph_canvas.draw()

	def on_build(self):
		x_start = int(self.from_entry.text())
		x_end = int(self.to_entry.text())
		x_var = self.x_dd.currentIndex()
		y_var = self.y_dd.currentIndex()

		# verify correct input
		if x_start > x_end:
			x_start, x_end = x_end, x_start
			self.from_entry.setText(str(x_start))
			self.to_entry.setText(str(x_end))
		if x_end > limits[x_var]:
			x_end = limits[x_var]
			self.to_entry.setText(str(x_end))

		x_end += 1
		inputs = self.parent().read_inputs_safe()

		res_x = range(x_start, x_end)
		res_y = []

		# no idea why, but original program worked like that
		if x_var == 1 and y_var == 4:
			res_x = [x_start, x_end]
			res_y = [0, 0]
			self.update_graph(res_x, res_y)
			return

		for i in res_x:
			inputs[x_var] = i
			all_traffic, channel_traffic = get_traffic(*inputs[:5])

			# dispatch table for y_var
			operations = {
				0: lambda: all_traffic,
				1: lambda: channel_traffic,
				2: lambda: erlang_c(all_traffic, inputs[3], inputs[5]),
				3: lambda: erlang_b(all_traffic, inputs[3]),
				4: lambda: erlang_a(all_traffic, inputs[3]),
			}
			res_y.append(operations[y_var]())

		self.update_graph(res_x, res_y)

class MplCanvas(FigureCanvas):
	def __init__(self, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)
