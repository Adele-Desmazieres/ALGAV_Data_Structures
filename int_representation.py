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
	
	def printuint(self) :
		print([x.value for x in self.val])
	
	def inf(cle1, cle2) :
		for i in range(3,-1,-1):
			if cle1.val[i].value < cle2.val[i].value: return True
		return False
	
	def inf_dynamic(self, x2) :
		return uint128.inf(self, x2)
	
	def eg(cle1, cle2) :
		for i in range (4):
			if cle1.val[i].value != cle2.val[i].value: return False
		return True
	
	def eg_dynamic(self, x2) :
		return uint128.eg(self, x2)

def test() :
	x1 = uint128(2**46)
	x2 = uint128(2**46)
	print(uint128.inf(x1, x2))
	print(uint128.inf(x2, x1))

	print(x1.inf_dynamic(x2))
	print(x2.inf_dynamic(x1))

	print(x1.inf(x2))
	print(x2.inf(x1))

	print(uint128.eg(x1, x2))
	print(uint128.eg(x2, x1))

	print(x1.eg_dynamic(x2))
	print(x2.eg_dynamic(x1))

	print(x1.eg(x2))
	print(x2.eg(x1))
	y = [1,2,3]
	x1.printuint()
	print(x1)
	


if __name__ == "__main__" :
	test()