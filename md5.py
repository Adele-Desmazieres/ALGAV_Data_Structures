import int_representation as ir

s = []
s[0:15] = [7,12,17,22] * 4
s[16:31] = [5,9,14,20] * 4
s[32:47] = [4,11,16,23] * 4
s[48:63] = [6,10,15,21] * 4

k = [None] * 64
for i in range(64) :
	k[i] = floor(2**32 * abs(math.sin(i+1)))

a0 = 0x67452301
b0 = 0xefcdab89
c0 = 0x98badcfe
d0 = 0x10325476

