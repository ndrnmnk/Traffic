import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIntValidator

from graph import GraphDisplay

from backend import *

limits = [1500, 1440, 100, 50, 3600, 100]

class Traffic(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Traffic")
		self.grid = QGridLayout()
		self.load_ui()

		main_widget = QWidget()
		main_widget.setLayout(self.grid)
		self.setCentralWidget(main_widget)

		self.show()

	def load_ui(self):
		# make entries
		default_values = ["1000", "1440", "20", "5", "20", "10"]

		# set up entries
		self.entries = [QLineEdit() for _ in range(6)]
		for idx, entry in enumerate(self.entries):
			entry.setValidator(QIntValidator(0, 1500))
			self.grid.addWidget(entry, idx, 1)
			entry.setText(default_values[idx])

		# add labels
		self.grid.addWidget(QLabel("Кількість абонентів:"), 0, 0)
		self.grid.addWidget(QLabel("Довжина робочого дня (хв):"), 1, 0)
		self.grid.addWidget(QLabel("Кількість сеансів зв'язку:"), 2, 0)
		self.grid.addWidget(QLabel("Кількість каналів:"), 3, 0)
		self.grid.addWidget(QLabel("Довжина сеансу зв'язку (с):"), 4, 0)
		self.grid.addWidget(QLabel("Вірогідність передзвону (%):"), 5, 0)
		# add a button
		self.calculate_btn = QPushButton("Розрахувати")
		self.calculate_btn.pressed.connect(self.on_calculate)
		self.grid.addWidget(self.calculate_btn, 6, 0)
		self.graph_btn = QPushButton("Графік")
		self.graph_btn.pressed.connect(lambda: GraphDisplay(self))
		self.grid.addWidget(self.graph_btn, 6, 1)
		# add result labels
		self.total_trafic_label = QLabel()
		self.channel_taffic_label = QLabel()
		self.pc_label = QLabel()
		self.pb_label = QLabel()
		self.pa_label = QLabel()
		self.grid.addWidget(QLabel("Трафік багатоканальної системи:"), 7, 0)
		self.grid.addWidget(self.total_trafic_label, 7, 1)
		self.grid.addWidget(QLabel("Трафік системи на канал:"), 8, 0)
		self.grid.addWidget(self.channel_taffic_label, 8, 1)
		self.grid.addWidget(QLabel("Вірогідність затримки зв'язку Pc:"), 9, 0)
		self.grid.addWidget(self.pc_label, 9, 1)
		self.grid.addWidget(QLabel("Вірогідність відмови системи Pb:"), 10, 0)
		self.grid.addWidget(self.pb_label, 10, 1)
		self.grid.addWidget(QLabel("Вірогідність відмови системи Pa:"), 11, 0)
		self.grid.addWidget(self.pa_label, 11, 1)

	def on_calculate(self):
		inputs = self.read_inputs_safe()


		all_traffic, channel_traffic = get_traffic(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4])
		chance_of_waiting = erlang_c(all_traffic, inputs[3], inputs[5])
		chance_of_blocking_pb = erlang_b(all_traffic, inputs[3])
		chance_of_blocking_pa = erlang_a(all_traffic, inputs[3])

		self.total_trafic_label.setText(str(round_2nd_digit(all_traffic)))
		self.channel_taffic_label.setText(str(round_2nd_digit(channel_traffic)))
		self.pc_label.setText(str(round_2nd_digit(chance_of_waiting)))
		self.pb_label.setText(str(round_2nd_digit(chance_of_blocking_pb)))
		self.pa_label.setText(str(round_2nd_digit(chance_of_blocking_pa)))

	def read_inputs_safe(self):
		inputs = []
		for idx, entry in enumerate(self.entries):
			t = int(entry.text())
			if t > limits[idx]:
				entry.setText(str(limits[idx]))
				t = limits[idx]
			inputs.append(t)
		return inputs

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle("Fusion")
	window = Traffic()
	sys.exit(app.exec_())