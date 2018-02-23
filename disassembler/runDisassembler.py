'''

@author: Kevin Walther
@assignment: RE/VA 695.744 Spring 2018 - Homework 2
@brief: This Python program implements a disassembler using a linear sweep algorithm.

'''

from Disassembler import Disassembler
import os
import sys

def processInputFile(inputFile):
	inputFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), inputFile)
	with open(inputFilePath, 'br') as fileId:
		disassembler = Disassembler(fileId)
		disassembler.processFile()
		disassembler.printInstructions()
		
# Begin code execution here.
if __name__ == "__main__":
	processInputFile('randomBinTest.o')
# 	print('Successful Completion!')
	






