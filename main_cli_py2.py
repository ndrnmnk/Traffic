from backend import *

def read_input(prompt, max_value):
    while True:
        try:
            t = int(raw_input(prompt))
        except ValueError:
            print("Only integers allowed")
            continue
        if 0 < t <= max_value:
            return t
        print("Number must be greater than 0 and less than", max_value)

abonents = read_input("Number of abonents: ", 1500)
workday = read_input("Workday length (min): ", 1440)
n_sessions = read_input("Number of sessions: ", 100)
n_channels = read_input("Number of channels: ", 50)
t_session = read_input("Session length (s): ", 3600)
p_retry = read_input("Retry probability (%): ", 100)

all_traffic, channel_traffic = get_traffic(abonents, workday, n_sessions, n_channels, t_session)
chance_of_waiting = erlang_c(all_traffic, n_channels, p_retry)
chance_of_blocking_pb = erlang_b(all_traffic, n_channels)
chance_of_blocking_pa = erlang_a(all_traffic, n_channels)

print("Multi-channel system traffic:", round_2nd_digit(all_traffic))
print("Traffic per channel:", round_2nd_digit(channel_traffic))
print("Chance of waiting Pc:", round_2nd_digit(chance_of_waiting))
print("Chance of system blocking Pb:", round_2nd_digit(chance_of_blocking_pb))
print("Chance of system blocking Pa:", round_2nd_digit(chance_of_blocking_pa))
raw_input("Press any key to exit...")
