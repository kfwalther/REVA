import os 

with open('randomBinTest.o', 'wb') as fout:
    fout.write(os.urandom(65536))
	
	