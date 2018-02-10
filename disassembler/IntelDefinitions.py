'''

@author: Kevin Walther
@assignment: RE/VA 695.744 Spring 2018 - Homework 2
@class: IntelDefinitions
@brief: This file stores some of the global Intel instruction definitions and relationships defined in the manual.

'''


# Intel extended register name to address map.
registerAddressDict = {
	'000': 'eax', 
	'001': 'ecx', 
	'010': 'edx', 
	'011': 'ebx', 
	'100': 'esp', 
	'101': 'ebp', 
	'110': 'esi', 
	'111': 'edi'
}

# Opcodes to instruction mnemonic map.
opcodeDict = {
	'add': ['01', '03', '05', '81'],
	'and': ['25', '81', '21', '23'],
	'call': ['E8', 'FF', '9A'],
	'clflush': ['0FAE'],
	'cmp': ['3D', '81', '39', '3B'],
	'dec': ['FF', '48'],
	'idiv': ['F7'],
	'imul': ['F7', '0FAF', '69'],
	'inc': ['FF', '40'],
	'jmp': ['EB', 'E9', 'FF', 'EA'],
	'jz': ['74', '0F84'],
	'jnz': ['75', '0F85'],
	'lea': ['8D'],
	'mov': ['89', '8B', 'A1', 'A3', 'B8', 'C7'],
	'movsd': ['A5'],
	'mul': ['F7'],
	'neg': ['F7'],
	'nop': ['90', '0F1F'],
	'not': ['F7'],
	'or': ['0D', '81', '09', '0B'],
	'out': ['EE', 'EF'],
	'pop': ['8F', '58', '1F', '07', '17', '0FA1', '0FA9'],
	'push': ['FF', '50', '68', '0E', '16', '1E', '06', '0FA0', '0FA8'],
	'repne cmpsd': ['F2A7'],
	'retf': ['CA', 'CB'],
	'retn': ['C2', 'C3'],
	'sal': ['D1'],
	'sar': ['D1'],
	'sbb': ['1D', '81', '19', '1B'],
	'shr': ['D1'],
	'test': ['A9', 'F7', '85'],
	'xor': ['35', '81', '31', '33']
}
# Opcodes to operand encoding map.
opcodeOpEnDict = {
	'M': ['E8', 'FF', '0FAE', 'F7', '0F1F', '8F'],
	'M1': ['D1'],
	'MI': ['81', 'C7', 'F7'],
	'MR': ['01', '31', '21', '39', '89', '09', '19', '85'],
	'RM': ['03', '23', '3B', '0FAF', '8D', '8B', '0B', '1B', '33'],
	'RMI': ['69'],
	'O': ['48', '40', '58', '50'],
	'I': ['05', '25', '3D', '0D', '68', 'C2', 'CA', '1D', 'A9', '35'],
	'OI': ['B8'],
	'D': ['9A', 'EB', 'E9', 'FF', 'EA', '74', '0F84', '75', '0F85'],
	'ZO': ['A5', '90', 'EE', 'EF', '1F', '07', '17', '0FA1', '0FA9', '0E', 
			'16', '1E', '06', '0FA0', '0FA8', 'F2A7', 'CB', 'C3'],
	'FD': ['A1'],
	'TD': ['A3']
}


# Define a list of opcodes that are accompanied by a MODRM byte.
modrmOpcodesList = ['01', '03', '09', '0B', '0F1F', '0FAF', '19', '1B', '21', '23', '31', '33', 
		'39', '3B', '69', '81', '85', '89', '8B', '8D', '8F', 'C7', 'D1', 'F7', 'FF'] 
# Define a list of instructions that often use a MODRM byte.
modrmInstructionsList = ['add', 'and', 'cmp', 'dec', 'idiv', 'imul', 
		'inc', 'jmp', 'lea', 'mov', 'mul', 'neg', 'nop', 'not', 'or', 
		'pop', 'push', 'sal', 'sar', 'sbb', 'shr', 'test', 'xor']