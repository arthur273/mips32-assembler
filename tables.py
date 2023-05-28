pseudoinstructions = {
    'move'  : ['add'],                
    'movn'  : ['bne', 'move'],
    'clear' : ['add'],                
    'li'    : ['addi', 'addi'],        
    'beq'   : ['lui', 'addi', 'beq'],  
    'ble'   : ['slt','bne'],    
    'bgt'   : ['slt','bne'],   
    'bge'   : ['slt','beq'],         
    'addi'  : ['addi','addi'],        
    'lw'    : ['addi','addi','lw']     
    }

# formato das instruções 

instructions = {
	'add'   : ['0x00','rs','rt','rd','shamt','0x20'],
	'addi'  : ['0x08','rs','rt','imm'],
	'addiu' : ['0x09','rs','rt','imm'],
	'addu'  : ['0x00','rs','rt','rd','shamt','0x21'],
	'and'   : ['0x00','rs','rt','rd','shamt','0x24'],
	'andi'  : ['0x0C','rs','rt','imm'],
	'beq'   : ['0x04','rs','rt','imm'],
	'bne'   : ['0x05','rs','rt','imm'],
    'clo'  : ['0x00','rs','rt','rd','shamt','0x11'],
	'j'     : ['0x02', 'add'],
	'jal'   : ['0x03', 'add'],
	'jr'    : ['0x00','rs','rt','rd','shamt','0x08'],
    'lb'   : ['0x20','rs','rt','imm'],
	'lbu'   : ['0x24','rs','rt','imm'],
	'lhu'   : ['0x25','rs','rt','imm'],
	'll'    : ['0x30','rs','rt','imm'],
	'lui'   : ['0x0F','rs','rt','imm'],
	'lw'    : ['0x23','rs','rt','imm'],
    'mul'   : ['0x1C','rs','rt','rd','shamt','0x02'],
	'nor'   : ['0x00','rs','rt','rd','shamt','0x27'],
	'or'    : ['0x00','rs','rt','rd','shamt','0x25'],
	'ori'   : ['0x0D','rs','rt','imm'],
    'sll'   : ['0x00','rs','rt','rd','shamt','0x00'],
    'srl'   : ['0x00','rs','rt','rd','shamt','0x02'],
    'sra'   : ['0x00','rs','rt','rd','shamt','0x03'],
    'srav'   : ['0x00','rs','rt','rd','shamt','0x07'],
	'slt'   : ['0x00','rs','rt','rd','shamt','0x2A'],
	'slti'  : ['0x0A','rs','rt','imm'],
    'sltiu' : ['0x0B','rs','rt','imm'],
	'sltu'  : ['0x00','rs','rt','rd','shamt','0x2B'],
	'sb'    : ['0x28','rs','rt','imm'],
	'sc'    : ['0x38','rs','rt','imm'],
	'sh'    : ['0x29','rs','rt','imm'],
    'sw'    : ['0x2B','rs','rt','imm'],
	'sub'   : ['0x00','rs','rt','rd','shamt','0x22'],
	'subu'  : ['0x00','rs','rt','rd','shamt','0x23'],
    'teq'  : ['0x00','rs','rt','rd','shamt','0x34'],
    'xor'  : ['0x00','rs','rt','rd','shamt','0x26'],
    'xori'  : ['0x0E','rs','rt','imm'],
    'div'   : ['0x00','rs','rt','rd','shamt','0x1A'],
	'divu'  : ['0x00','rs','rt','rd','shamt','0x1B'],
    'mfhi'  : ['0x00','rs','rt','rd','shamt','0x10'],
	'mflo'  : ['0x00','rs','rt','rd','shamt','0x12']
	}

# registradores

registers = {
	'$zero' : 0,
	'$at' : 1,
	'$v0' : 2,
	'$v1' : 3,
	'$a0' : 4,
	'$a1' : 5,
	'$a2' : 6,
	'$a3' : 7,
	'$t0' : 8,
	'$t1' : 9,
	'$t2' : 10,
	'$t3' : 11,
	'$t4' : 12,
	'$t5' : 13,
	'$t6' : 14,
	'$t7' : 15,
	'$s0' : 16,
	'$s1' : 17,
	'$s2' : 18,
	'$s3' : 19,
	'$s4' : 20,
    '$s5' : 21,
	'$s6' : 22,
	'$s7' : 23,
	'$t8' : 24,
	'$t9' : 25,
	'$k0' : 26,
	'$k1' : 27,
    '$gp' : 28,
	'$sp' : 29,
	'$fp' : 30,
    '$ra' : 31
	}


#Layouts dos 3 tipos de instruçao
layouts = { 
    '6' : [6,5,5,5,5,6], #tipo R
    '4' : [6,5,5,16], #tipo I
    '2' : [6,26] #tipo J
}