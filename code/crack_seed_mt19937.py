import random
import time
from implement_mt19937 import MT19937

min_sleep_time, max_sleep_time = 40, 100

def main():
	sleep_time_1 = random.randint(min_sleep_time, max_sleep_time)
	print("Sleep time 1: ", sleep_time_1)
	time.sleep(sleep_time_1)
	seed1 = int(time.time())
	rng = MT19937(seed1)
	print("Actual seed: ", seed1)
	sleep_time_2 = random.randint(min_sleep_time, max_sleep_time)
	print("Sleep time 2: ", sleep_time_2)
	time.sleep(sleep_time_2)
	number = rng.temper()
	# print("Number: ", number)

	cur_time = int(time.time())
	seed2 = cur_time
	for i in range(cur_time - max_sleep_time, cur_time - min_sleep_time):
		rng = MT19937(i)
		tmp_num = rng.temper()
		# print("Seed:", i, " Number: ", tmp_num)
		if tmp_num == number:
			seed2 = i
			print("Guessed seed: ", seed2)
			break
	test_seeds(seed1, seed2)

def test_seeds(seed1, seed2, lim = 100000):
	compare_RNGs(MT19937(seed1), MT19937(seed2))

def compare_RNGs(r1, r2, lim = 100000):
	for i in range(lim):
		if(r1.temper() != r2.temper()):
			print("RNGs not the same; stopped at index ", i)
			return
	print("From inspecting the first ", lim, " numbers, the two RNGs are the same.")

if __name__ == '__main__':
	main()