import ctypes

# unsigned int with a list of 4 uint32, from weaker to stronger bits
class uint128 :
	
	def __init__(self, intval) :
		mask = (2**32 - 1)
		val1 = intval & mask
		val2 = (intval >> 32) & mask
		val3 = (intval >> 64) & mask
		val4 = (intval >> 96) & mask
		
		self.val = [ctypes.c_uint32(val1), ctypes.c_uint32(val2), ctypes.c_uint32(val3), ctypes.c_uint32(val4)]
		self.size = len(self.val)
	
	def __eq__(self, x2) :
		for i in range(self.size):
			if self.val[i].value != x2.val[i].value: 
				return False
		return True
	
	def __ne__(self, x2) :
		return not (self == x2)
	
	def __lt__(self, x2) :
		for i in range(self.size-1, -1, -1):
			if self.val[i].value < x2.val[i].value:
				return True
			elif self.val[i].value > x2.val[i].value:
				return False
		return False
	
	def __le__(self, x2) :
		return (self < x2) or (self == x2)
	
	def __gt__(self, x2) :
		return (x2 < self)
	
	def __ge__(self, x2) :
		return (x2 <= self)
	
	def __str__(self) :
		return str(self.val)


def test() :
	x1 = uint128(2**46)
	x2 = uint128(2**46)
	x3 = uint128(2**46 - 1)
	
	print("x1 =", x1)
	print("x2 =", x2)
	print("x3 =", x3)
	
	assert((x1 == x2) == True)
	assert((x1 == x3) == False)
	assert((x1 < x2) == False)
	assert((x1 < x3) == False)
	assert((x1 <= x2) == True)
	assert((x1 <= x3) == False)
	assert((x1 > x2) == False)
	assert((x1 > x3) == True)
	assert((x1 >= x2) == True)
	assert((x1 >= x3) == True)
	
	print("Tous les tests sont valides.")


if __name__ == "__main__" :
	test()