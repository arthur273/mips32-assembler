import sys
import re
from tables import layouts, instructions, pseudoinstructions, registers

class assembler(object):

    # 1 word = 4 bytes

    word_size = 4

    default_mem_loc = 0

    # labels e seus locais na memória
    symbols = {}

    # local na atual da memória
    current_location  = 0

    # tabelas
    registers = {}
    pseudoinstructions = {}
    instructions = {}
    layouts= {}

    # array com as instruções
    array2D = []

    #final

    final = []

    def __init__(self, default_memory_loc, instructions, registers, pseudoinstructions, layouts, word_size): 
        self.default_mem_loc = default_memory_loc
        self.instructions = instructions
        self.registers = registers
        self.pseudoinstructions  = pseudoinstructions
        self.word_size = word_size
        self.layouts = layouts

    def first_pass(self, lines):
        for line in lines:
            # Reconhecer e alocar labels
            if ':' in line:
                label = line[0:line.find(':')]
                self.symbols[label] = str(self.current_location)
                line = line[line.find(':') + 1:].strip() #retira a label da linha e limpa espaços em branco nas extremidades

            # determinar instrução para alocar memória
            instruction = line[0:line.find(' ')]
            arguments = line[line.find(' ') + 1:].replace(' ', '').split(',')
            i = 0
            for arg in arguments:
                if "$" not in arg:
                    if 'x' in arg:
                        arguments[i] = int(arg, 16)
                    else:
                        arguments[i] = int(arg, 10)
                i += 1
            self.current_location = self.current_location + self.instruction_size(instruction, arguments)

    def instruction_size(self, instruction, args):
            ''' Calculate instruction size for first pass in bytes
            '''

            if instruction in self.pseudoinstructions:
                # check overload
                if instruction == 'beq':
                    if not '$' in args[1]:
                        if self.value_outside_range(int(args[1])):
                            return 12
                        else:
                            return 8
                    else:
                        return 4

                # check for size of argument
                if instruction == 'li':
                    if self.value_outside_range(int(args[1])):
                        return 8
                    else:
                        return 4

                if instruction == 'addi':
                    if self.value_outside_range(int(args[2])):
                        return 12
                    else:
                        return 4

                if instruction == 'lw':
                    if '(' in args[1]:
                        offset = int(args[1][0:args[1].find('(')])
                        if self.value_outside_range(offset):
                            return 12
                        else:
                            return 4

                # Branch instructions will always be same amount of regular instructions
                if instruction == 'bgt' or instruction == 'ble' or instruction == 'bge' or instruction == 'movn':
                    return 8

                # move and clear always are 4 bytes
                return 4
            if instruction in self.instructions:
                return 4
            else:
                print("NOT VALID INSTRUCTION: " + instruction + "\n ABORTING...")
                exit()

    def second_pass(self, lines):
        # Essa função deve montar um array de arrays com o formato correto das instruções a serem executadas
        for line in lines:
            if '\n' in line:
                line = line[:line.find('\n') + 1].strip()
            if ':' in line:
                label = line[0:line.find(':')]
                line = line[line.find(':') + 1:].strip()

            # Determinar instrução e argumentos
            instruction = line[0:line.find(' ')]
            arguments = line[line.find(' ') + 1:].replace(' ', '').split(',')
            if instruction in self.pseudoinstructions:
                self.parse_pseudoinstruction(instruction, arguments)
            elif instruction in self.instructions:
                self.parse_instruction(instruction, arguments)
    def machine_code(self):
        for line in self.array2D:
            i = 0
            instruction_size = str(len(line)) #Para determinar o tipo de instrução
            layout = layouts[instruction_size]
            binary_line = ''
            # transformação para base binária

            while i < len(line):
                if type(line[i]) != int:
                    if 'x' in line[i]:
                        line[i] = int(line[i][2:],16)
                    elif '$' in line[i]:
                        line[i] = self.registers[line[i]]
                line[i] = str(self.to_binary(line[i])) # to_binary deve receber numeros em hexadecimal em forma de string ou decimal
                # formataçao em layout correto
                binary_line += self.set_string_size(line[i], layout[i])

                i = i + 1

            # converter para hexadecimal
            binary_line = int(binary_line,2)
            hex_line = self.set_string_size(hex(binary_line)[2:], 8)
            self.final.append(hex_line)

    def parse_instruction(self, instruction, arguments):
        array = self.instructions[instruction] # array contem o formato da instrução
        offset = 'NaN'
        argument_iterator = 0

        for arg in arguments:
            if type(arg) == int:
                continue
            if '(' in arg:

                offset   = hex(int(arg[0:arg.find('(')]))
                register = re.search('\((.*)\)', arg).group(1)
                arguments[argument_iterator] = register

            elif arg in self.symbols:
                arguments[argument_iterator] = int(self.symbols[arg])

            argument_iterator += 1

        if len(array) == 6:
            rs = 0
            rt = 0
            rd = 0
            if len(arguments) == 1:
                rs = arguments[0]
            elif len(arguments) > 2:
                rs = arguments[1]
                rt = arguments[2]
                rd = arguments[0]
            array[1] = rs
            array[2] = rt
            array[3] = rd
            array[4] = '0'

        if len(array) == 4:
            rs  = arguments[1]
            rt  = arguments[0]
            imm = offset

            if len(arguments) == 3:
                if type(arguments[2]) != int:
                    imm = hex(int(arguments[2], 16))

            elif imm == 'NaN':
                imm = arguments[1]
                rs = '0'

            array[1] = rs
            array[2] = rt
            array[3] = imm

        if len(array) == 2:
            address = arguments[0]
            array[1] = hex(int(address, 16))


        self.array2D.append(array)

    def parse_pseudoinstruction(self, pseudo_ins , args):

        instruction_list = [] # arrays para as instruções e argumentos das instruções que compoem as pseudo-instruções
        argument_list = []



        i = 0
        for arg in args:
            if "$" not in arg:
                if 'x' in arg:
                    args[i] = int(arg, 16)
                else:
                    args[i] = int(arg, 10)
            i += 1

        if pseudo_ins == 'beq':
            if not '$' in args[1]:
                if self.value_outside_range(int(args[1])):
                    lower_16 = int(int(args[1]) % pow(2, 16))
                    upper_16 = int(int(args[1]) / pow(2, 16))
                    instruction_list = ['lui', 'ori', 'beq']
                    argument_list    = [['$at', str(upper_16)],
                                    ['$at', '$at', str(lower_16)],
                                    ['$at', args[0], args[2]]]

                else:
                    instruction_list = ['addi', 'beq']
                    argument_list    = [[args[0], args[0], args[1]],
                                    [args[0], args[0], args[2]]]
            else:
                instruction_list.append(pseudo_ins)
                argument_list.append(args)

        if pseudo_ins == 'li':
            if self.value_outside_range(args[1]):
                    lower_16 = int(int(args[1]) % pow(2, 16))
                    upper_16 = int(int(args[1]) / pow(2, 16))
                    instruction_list = ['lui', 'ori']
                    argument_list    = [['$at', str(upper_16)], [args[0], '$at', str(lower_16)]]
            else:
                    instruction_list = ['addi']
                    argument_list    = [[args[0], '$zero', args[1]]]


        if pseudo_ins == 'addi':
            if self.value_outside_range(int(args[2])):
                 lower_16 = int(int(args[2]) % pow(2, 16))
                 upper_16 = int(int(args[2]) / pow(2, 16))
                 instruction_list = ['lui', 'addi', 'add']
                 argument_list    = [[args[0], str(upper_16)],
                                 [args[0], args[0], str(lower_16)],
                                 [args[0], args[0], args[1]]]
            else:
                instruction_list.append(pseudo_ins)
                argument_list.append(args)


        if pseudo_ins == 'lw':
            if '(' in args[1]:
                offset = int(args[1][0:args[1].find('(')])
                register = re.search('\((.*)\)', args[1]).group(1)
                if self.value_outside_range(offset):
                    lower_16 = offset % pow(2, 16)
                    upper_16 = offset / pow(2, 16)
                    instruction_list = ['lui', 'addi', 'lw']
                    argument_list    = [[args[0], str(upper_16)],
                                    [args[0], register, '$zero'],
                                    [args[0], str(lower_16)+"("+register+")"]]
                else:
                    instruction_list.append(pseudo_ins)
                    argument_list.append(args)

        # same amount as regular instructions
        if pseudo_ins == 'bge':
            instruction_list = ['slt', 'beq']
            argument_list = [[args[0], args[0], args[1]], [args[0], '$zero', args[2]]]

        if pseudo_ins == 'bgt':
            instruction_list = ['slt', 'bne']
            argument_list = [[args[0], args[0], args[1]], [args[0], '$zero', args[2]]]

        if pseudo_ins == 'ble':
            instruction_list = ['slt', 'bne']
            argument_list = [[args[0], args[1], args[0]], [args[0], '$zero', args[2]]]

        if pseudo_ins == 'move':
            instruction_list = ['add']
            argument_list = [[args[0], args[1], '$zero']]

        if pseudo_ins == 'clear':
            instruction_list = ['add']
            argument_list = [[args[0], '$zero', '$zero']]

        instruction_iterator = 0
        while instruction_iterator < len(instruction_list):
            self.parse_instruction(instruction_list[instruction_iterator], argument_list[instruction_iterator])
            instruction_iterator += 1
        return 0


    def value_outside_range(self, value):
        # check if value > 16  bits
        if type(value) == str:
            if 'x' in value:
                value = int(value[2:], 16)


        if abs(value) > pow(2,32):
            print("The value: " + str(value) + " is greater than 32-bits! ERROR")
            exit()

        return value > (pow(2, 15) - 1) or value < -(pow(2, 15))


    def to_binary(self, number):
        #para hexadecimal
        binary_number = "undefined"
        if type(number) is str:
            if 'x' in number:
                hex_number = int(number, 16)  # hexadecimal to decimal
                binary_number = bin(hex_number)[2:]  # decimal to binary and remove '0b'
            else:
                decimal_number = int(number, 10)
                binary_number = bin(decimal_number)[2:]  
        if type(number) is int:
            binary_number = bin(number)[2:] 
        return binary_number

    def set_string_size(self, bin_number, size):
        return   ((size - len(bin_number)) * "0") + bin_number


def create_file(file_path, file_contents):
    try:
        with open(file_path, 'w') as file:
            file.write(file_contents)
        return True
    except IOError:
        return False

path = "/text.mif"
