e = 2.718281828459045

def erlang_b(total_traffic, num_channels):
	numerator = 100 * (total_traffic ** num_channels)
	denominator = factorial(num_channels) * sum((total_traffic ** k) / float(factorial(k)) for k in range(num_channels + 1))
	return numerator / denominator


def erlang_c(total_traffic, num_channels, retry_chance):
	if total_traffic >= num_channels:
		return 100.0
	numerator = retry_chance * total_traffic ** num_channels
	denominator = factorial(num_channels - 1) * (num_channels - total_traffic)
	return min(numerator / denominator, 100.0)

def erlang_a(total_traffic, num_channels):
	t1 = 1.0 / (num_channels+1)
	t2 = t1 / (num_channels+2)
	numinator = 100 * total_traffic * (1 + t1 + t2)
	try:
		denominator = factorial(num_channels) * e**total_traffic
	except OverflowError: return 0
	return float(numinator) / denominator

def get_traffic(abonents, workday, n_sessions, n_channels, t_session):
	all_traffic = float(abonents) * n_sessions * t_session / (workday * 60)
	channel_traffic = all_traffic / n_channels

	return all_traffic, channel_traffic

def factorial(n):
	result = 1
	for i in range(2, n+1):
		result *= i
	return result

def round_2nd_digit(n):
	return int(n*100)/100.0