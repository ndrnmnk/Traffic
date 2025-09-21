from backend import *

def read_input(prompt, max_value):
	while True:
		try:
			t = int(input(prompt))
		except ValueError:
			print("Можна ввести лише цілі числа")
			continue
		if 0 < t <= max_value:
			return t
		print(f"число має бути більше за нуль і менше за {max_value}")

abonents = read_input("Кількість абонентів: ", 1500)
workday = read_input("Довжина робочого дня (хв): ", 1440)
n_sessions = read_input("Кількість сеансів зв'язку: ", 100)
n_channels = read_input("Кількість каналів: ", 50)
t_session = read_input("Довжина сеансу зв'язку (с): ", 3600)
p_retry = read_input("Вірогідність передзвону (%): ", 100)

all_traffic, channel_traffic = get_traffic(abonents, workday, n_sessions, n_channels, t_session)
chance_of_waiting = erlang_c(all_traffic, n_channels, p_retry)
chance_of_blocking_pb = erlang_b(all_traffic, n_channels)
chance_of_blocking_pa = erlang_a(all_traffic, n_channels)


print("Трафік багатоканальної системи:", round(all_traffic, 2))
print("Трафік системи на канал:", round(channel_traffic, 2))
print("Вірогідність затримки зв'язку Pc:", round(chance_of_waiting, 2))
print("Вірогідність відмови системи Pb:", round(chance_of_blocking_pb, 2))
print("Вірогідність відмови системи Pa:", round(chance_of_blocking_pa, 2))