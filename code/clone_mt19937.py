from implement_mt19937 import MT19937

def get_bit(x, i):
	return (x & (1 << (MT19937.w - i - 1)))

def reverse_bits(x):
	rev = 0
	for i in range(MT19937.w):
		rev = (rev << 1)
		if(x > 0):
			if (x & 1 == 1):
				rev = (rev ^ 1)
			x = (x >> 1)
	return rev

def inv_left(y, a, b):
	return reverse_bits(inv_right(reverse_bits(y), a, reverse_bits(b)))

def inv_right(y, a, b):
	x = 0
	for i in range(MT19937.w):
		if (i < a):
			x |= get_bit(y, i)
		else:
			x |= (get_bit(y, i) ^ ((get_bit(x, i - a) >> a) & get_bit(b, i)))
	return x

def untemper(y):
	x = y
	x = inv_right(x, MT19937.l, ((1 << MT19937.w) - 1))
	x = inv_left(x, MT19937.t, MT19937.c)
	x = inv_left(x, MT19937.s, MT19937.b)
	x = inv_right(x, MT19937.u, MT19937.d)
	return x

def compare_RNGs(r1, r2, lim = 100000):
	for i in range(lim):
		if(r1.temper() != r2.temper()):
			print("RNGs not the same; stopped at index ", i)
			return
	print("From inspecting the first ", lim, " numbers, the two RNGs are the same.")

def main():
	rng1 = MT19937(0)
	rng2 = MT19937(1)
	for i in range(MT19937.n):
		rng2.X[i] = untemper(rng1.temper())
	rng2.twist()
	compare_RNGs(rng1, rng2)

if __name__ == '__main__':
	main()