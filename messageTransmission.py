def module2(dividend, divisor):

	quotient = 0
	k = dividend.bit_length()
	r = divisor.bit_length()
	aux = k - r

	# shifting the divided
	rest = dividend >> (aux)

	while aux > -1:

		bits = rest.bit_length()

		quotient <<= 1
		if bits == r:
			quotient |= 1
			rest ^= divisor
			print "%s%9s%s" %((k - r - aux) * ' ', bin(divisor), (aux) )
		else:
			print "%s%s%s" % ((k - r - aux) * ' ', "0b0000000", (aux) )
		print  "%s%s%s" % ((k - r - aux) * ' ',"---------", (aux) )

		aux -= 1
		if aux > -1:
			rest  = ((rest << 1) | ((dividend >> aux) & 1))
		print "%s%9s%s" % ((k - r - aux) * ' ', bin(rest), (aux))

	return (quotient, rest)

if __name__ == '__main__':
	
	message = 0b11001101001101010010111010010110 #the original message
	polynom = 0b1110011

	k = message.bit_length() #message size
	r = polynom.bit_length() #polynom size

	completeMessage = message << (r - 1) #shiftind the message r bits as the crc method
	quotient, fcs = module2(completeMessage, polynom) #obtaining the quocient and rest by module 2 division
	transmission = completeMessage ^ fcs #message k+r bits to be transmitted
	
	print "\nFCS:", bin(fcs)
	print "Transmits:", bin(transmission)


	print "\ncrc recepted"
	_, rest = module2(transmission, polynom) 

	print "\nTransmitted" if rest == 0 else "it failed"

	print "r5 / r4 / r3 / r2 / r1  r0 / r54i / r53i / r50i / r5i / i \n\n"  
	r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0

	for j in range(32):
		i = (message >> 31 - j) & 1
		
		r5i = r5 ^ i
		r50i = r5 ^ i ^ r0
		r53i = r5 ^ i ^ r3
		r54i = r5 ^ i ^ r4

		print "%2d %3d %3d %3d %3d %3d  %3d   %3d   %3d   %2d   %d" %(r5, r4, r3, r2, r1, r0, r54i, r53i, r50i, r5i, i)

		r5 = r54i
		r4 = r53i
		r3 = r2
		r2 = r1
		r1 = r50i
		r0 = r5i

	print "%2d %3d %3d %3d %3d %3d " %(r5, r4, r3, r2, r1, r0)  #lfsr table
 