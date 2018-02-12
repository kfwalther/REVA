'''

@author: Kevin Walther
@class: RE/VA 695.744 Spring 2018
@assignment: Homework 2
@brief: This Python program implements a disassembler.

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
	processInputFile('example2.o')
	print('Successful Completion!')
	






