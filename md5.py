import math
import int_representation as ir
import hashlib


def leftrotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5(message):
	s = []
	s[0:15] = [7,12,17,22] * 4
	s[16:31] = [5,9,14,20] * 4
	s[32:47] = [4,11,16,23] * 4
	s[48:63] = [6,10,15,21] * 4

	k = [None] * 64
	for i in range(64) :
		k[i] = math.floor(2**32 * abs(math.sin(i+1)))

	a0 = 0x67452301
	b0 = 0xefcdab89
	c0 = 0x98badcfe
	d0 = 0x10325476

	x = 8 * len(message)
	message += b'\x80'
	while (len(message) * 8) % 512 != 448:
		message += b'\x00'

	message += x.to_bytes(8, 'little')

	for i in range(0, len(message), 64):
		chunk = message[i : i + 64]
		M = [int.from_bytes(chunk[j:j+4], byteorder='little') for j in range(0, 64, 4)]

		A, B, C, D = a0, b0, c0, d0

		for j in range(64):
			if 0 <= j <= 15:
				F = (B & C) | ((~B) & D)
				g = j
			elif 16 <= j <= 31:
				F = (D & B) | ((~D) & C)
				g = (5 * j + 1) % 16
			elif 32 <= j <= 47:
				F = B ^ C ^ D
				g = (3 * j + 5) % 16
			elif 48 <= j <= 63:
				F = C ^ (B | (~D))
				g = (7 * j) % 16

			F = (F + A + k[j] + M[g]) & 0xFFFFFFFF
			A = D
			D = C
			C = B
			B = (B + leftrotate(F, s[j])) & 0xFFFFFFFF

		a0 = (a0 + A) & 0xFFFFFFFF
		b0 = (b0 + B) & 0xFFFFFFFF
		c0 = (c0 + C) & 0xFFFFFFFF
		d0 = (d0 + D) & 0xFFFFFFFF

	digest = a0.to_bytes(4, byteorder='little') + \
			 b0.to_bytes(4, byteorder='little') + \
			 c0.to_bytes(4, byteorder='little') + \
			 d0.to_bytes(4, byteorder='little')

	return digest

def test():
	message = b"OMG THE FUNCTION IS DONE FINALLY"
	result = md5(message)
	print(result.hex())
	
	result = hashlib.md5(b"OMG THE FUNCTION IS DONE FINALLY") 
	print(result.digest().hex())

if __name__=="__main__" :
	test()
