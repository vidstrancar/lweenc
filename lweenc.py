import random
import numpy
import math


def str_to_bits(s):
	b = []
	for c in s:
		bits = bin(ord(c))[2:]
		bits = '00000000'[len(bits):] + bits
		b.extend([int(b) for b in bits])
	return b
def bits_to_str(bits):
	s = []
	for b in range(len(bits) // 8):
		byte = bits[b*8:(b+1)*8]
		s.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(s)	
def is_prime(n):
	if n == 2:
		return True
	if n % 2 == 0 or n <= 1:
		return False

	sqr = int(math.sqrt(n)) + 1

	for divisor in range(3, sqr, 2):
		if n % divisor == 0:
			return False
	return True
def dot(x, y):
	s = 0
	for a,b in zip(x,y):
		s+= a*b
	return s
def vector_addition(x,y):
	l = []
	for a,b in zip(x,y):
		l.append(a+b)
	return l
def vector_mod(x, q):
	l = []
	for a in x:
		l.append(a%q)
	return l

class Discrete_gaussian_distribution:
	def __init__(self, s, q):
		self.s = s
		self.q = q
	def sample(self):
		x = numpy.random.normal(0, self.s)
		return round(x)%self.q

class Lwe_encryptor:
	def __init__(self, n, q, m, A):
		self.A = numpy.array(A)
		self.q = q
		self.n = n
		self.m = m	
	def encrypt_bit(self, p):
		c = [0 for _ in range(self.n+1)]
		for lwe_sample in self.A:
			if random.randint(0,1) == 1:
				c = numpy.array(vector_addition(c, lwe_sample))
		if p == 1:
			c[self.n]+= math.floor(self.q/2)
		c = c.tolist()
		return vector_mod(c, self.q)
	def encrypt(self, s):
		encrypted = []
		bits = str_to_bits(s)
		for b in bits:
			encrypted.append(self.encrypt_bit(b))
		return encrypted

class Lwe_decryptor:
	def __init__(self, n, q=None, m=None, alpha=None, s=None, A=None):
		self.n = n
		if q == None:
			self.q = self.param_q_setup(self.n)
		else:
			self.q = q
		if m == None:
			self.m = self.param_m_setup(self.n, self.q)
		else:
			self.m = m
		if alpha == None:
			self.alpha = self.param_alpha_setup(self.n)
		else:
			self.alpha = alpha
		if s == None or A == None:
			self.keyGen()
		else:
			self.s = s
			self.A = A	
	def param_q_setup(self, n):
		for q in range(n, n**2+1):
			if is_prime(q):
				return q
	def param_m_setup(self, n, q):
		return math.ceil(1.1*n*math.log(q))
	def param_alpha_setup(self, n):
		return 1/(math.sqrt(n)*math.log(n)**2)	
	def keyGen(self):
		self.s = [random.randint(0, self.q-1) for _ in range(self.n)]
		self.A = self.lwe_sample(self.m)
	def lwe_sample(self, N):
		DGD = Discrete_gaussian_distribution(self.alpha*self.q, self.q)
		A = []
		for _ in range(N):
			a = [random.randint(0, self.q-1) for _ in range(self.n)]
			e = DGD.sample()
			b = (dot(self.s,a)+e) % self.q
			a.append(b)
			A.append(a)
		return A
	def decrypt_bit(self, c):
		k = (c[self.n] - dot(self.s, c[0:self.n]))%self.q
		p = math.floor(self.q/2)
		if min(k%self.q, -k%self.q) < min((p-k)%self.q, (k-p)%self.q):
			return 0
		else:
			return 1
	def decrypt(self, encrypted):
		bits = []
		for b in encrypted:
			bits.append(self.decrypt_bit(b))
		return bits_to_str(bits)





#n=100
#ld = Lwe_decryptor(n)
#le = Lwe_encryptor(ld.n, ld.q, ld.m, ld.A)
#s = 'P0zdravljen, svet!'
#encrypted = le.encrypt(s)
#decrypted = ld.decrypt(encrypted)
#print(decrypted)



# st_poskusov = 100
# st_uspesnih = 0
# p1 = 1
# for _ in range(st_poskusov):
	# ld = Lwe_decryptor(n, q, m, alpha)
	# print(ld.A)
	# print(ld.s)
	# le = Lwe_encryptor(ld.A, ld.q, ld.n, ld.m)
	# c = le.encrypt_bit(p1)
	# print(p1, " -e> ", c)
	# p2 = ld.decrypt_bit(c)
	# print(c, " -d> ", p2)
	# print()
	# if p2 == p1:
		# st_uspesnih+=1		
# print("decryption success rate: ", st_uspesnih/st_poskusov)
