class MT19937:

	w, n = 32, 624
	f = 1812433253
	m, r = 397, 31
	a = 0x9908B0DF
	d, b, c = 0xFFFFFFFF, 0x9D2C5680, 0xEFC60000
	u, s, t, l = 11, 7, 15, 18

	def __init__(self, seed):
		self.X = [0] * MT19937.n
		self.cnt = 0
		self.initialize(seed)

	def initialize(self, seed):
		self.X[0] = seed
		for i in range(1, MT19937.n):
			self.X[i] = (MT19937.f * (self.X[i - 1] ^ (self.X[i - 1] >> (MT19937.w - 2))) + i) & ((1 << MT19937.w) - 1)
		self.twist()

	def twist(self):
		for i in range(MT19937.n):
			lower_mask = (1 << MT19937.r) - 1
			upper_mask =  (~lower_mask) & ((1 << MT19937.w) - 1)
			tmp = (self.X[i] & upper_mask) + (self.X[(i + 1) % MT19937.n] & lower_mask)
			tmpA = tmp >> 1
			if (tmp % 2):
				tmpA = tmpA ^ MT19937.a
			self.X[i] = self.X[(i + MT19937.m) % MT19937.n] ^ tmpA
		self.cnt = 0

	def temper(self):
		if self.cnt == MT19937.n:
			self.twist()
		y = self.X[self.cnt]
		y = y ^ ((y >> MT19937.u) & MT19937.d)
		y = y ^ ((y << MT19937.s) & MT19937.b)
		y = y ^ ((y << MT19937.t) & MT19937.c)
		y = y ^ (y >> MT19937.l)
		self.cnt += 1
		return y & ((1 << MT19937.w) - 1)

def main():
	rng = MT19937(0)
	for i in range(10):
		print(rng.temper())

if __name__ == '__main__':
	main()