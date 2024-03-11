opcode_list = {
    'add': '0110011',
    'sub': '0110011',
    'lw': '0000011',
    'sw': '0100011',
    'addi': '0010011',
    'sltiu': '0010011',
    'jalr': '1100111',
    'auipc': '0010111',
    'lui': '0110111',
    'jal': '1101111',
    'sll': '0110011',
    'sltu': '0110011',
    'slt': '0110011',
    'xor': '0110011',
    'or': '0110011',
    'and': '0110011',
    'srl': '0110011',
    'beq': '1100011',
    'bne': '1100011',
    'bge': '1100011',
    'bgeu': '1100011',
    'blt': '1100011',
    'bltu': '1100011'
}

funct3_list = {
    'add': '000',
    'sub': '000',
    'slt': '010',
    'sltu': '011',
    'sll': '001',
    'srl': '101',
    'xor': '100',
    'or': '110',
    'and': '111',
    'lw': '010',
    'sw': '010',
    'addi': '000',
    'sltiu': '011',
    'jalr': '000',
    'auipc': '000',
    'lui': '000',
    'jal': '000',
    'beq': '000',
    'bne': '001',
    'bge': '101',
    'bgeu': '111',
    'blt': '100',
    'bltu': '110'
}

register_list = {
    'zero': '00000',  # x0
    'ra': '00001',    # x1
    'sp': '00010',    # x2
    'gp': '00011',    # x3
    'tp': '00100',    # x4
    't0': '00101',    # x5
    't1': '00110',    # x6
    't2': '00111',    # x7
    's0': '01000',    # x8
    's1': '01001',    # x9
    'a0': '01010',    # x10
    'a1': '01011',    # x11
    'a2': '01100',    # x12
    'a3': '01101',    # x13
    'a4': '01110',    # x14
    'a5': '01111',    # x15
    'a6': '10000',    # x16
    'a7': '10001',    # x17
    's2': '10010',    # x18
    's3': '10011',    # x19
    's4': '10100',    # x20
    's5': '10101',    # x21
    's6': '10110',    # x22
    's7': '10111',    # x23
    's8': '11000',    # x24
    's9': '11001',    # x25
    's10': '11010',   # x26
    's11': '11011',   # x27
    't3': '11100',    # x28
    't4': '11101',    # x29
    't5': '11110',    # x30
    't6': '11111'     # x31
}

def assembler(instruction):
    parts2 = instruction.strip().split(' ')
    opcode = opcode_list[parts2[0]]
    parts = parts2[1].strip().split(',')
    if parts2[0] in ['add', 'sub', 'slt', 'sltu', 'srl', 'sll', 'xor', 'or', 'and', 'lw', 'sw', 'addi', 'sltiu']:
        funct3 = funct3_list[parts2[0]]
        rd = register_list[parts[0]]
        if parts2[0] == 'addi' or parts2[0] == 'sltiu':
            rs = register_list[parts[1]]
            imm = int(parts[2])
            binary_imm = format(imm & 0b111111111111, '012b')
            return binary_imm, rs, funct3, rd, opcode
        elif parts2[0] == 'lw':
            immediate_str, register_str = parts[1].split('(')
            register_str = register_str.strip(')')
            imm = int(immediate_str)
            binary_imm = format(imm & 0b111111111111, '012b')
            rs = register_list[register_str]
            return binary_imm, rs, funct3, rd, opcode
        elif parts2[0] == 'sw':
            immediate_str, register_str = parts[1].split('(')
            register_str = register_str.strip(')')
            imm = int(immediate_str)
            rs1 = register_list[register_str]
            rs2 = register_list[parts[0]]
            binary_imm = bin(imm & 0xFF)[2:].zfill(12)
            binary_imm.split()
            return binary_imm[1:7], rs2, rs1, funct3_list[parts2[0]], binary_imm[7:12], opcode
        else:
            rs1 = register_list[parts[1]]
            rs2 = register_list[parts[2]]
            if parts2[0] == 'sub':
                funct7 = '0100000'
            else:
                funct7 = '0000000'
            return funct7, rs2, rs1, funct3, rd, opcode

    elif parts2[0] == 'jalr':
        rd = register_list[parts[0]]
        rs = register_list[parts[1]]
        imm = int(parts[2])
        binary_imm = format(imm & 0b11111111111, '011b')
        return '0', binary_imm, rs, '000', rd, opcode
    elif parts2[0] == 'auipc' or parts2[0] == 'lui':
        rd = register_list[parts[0]]
        imm = int(parts[1])
        binary_imm = format(imm & 0b11111111111111111111, '020b')
        return binary_imm, rd, opcode
    elif parts2[0] == 'jal':
        rd = register_list[parts[0]]
        imm = int(parts[1])
        binary_imm = format(imm & 0b11111111111111111111, '020b')
        return binary_imm, rd, opcode
    
    elif parts2[0] in ['beq', 'bne', 'bge', 'bgeu', 'blt', 'bltu']:
        rs1 = register_list[parts[0]]
        rs2 = register_list[parts[1]]
        imm = int(parts[2])
        imm_upper = (imm >> 5) & 0b111111
        imm_upper |= ((imm >> 11) & 0b1) << 6
        imm_lower = ((imm >> 1) & 0b1111) | ((imm >> 11) & 0b1) << 4
        binary_imm_upper = format(imm_upper, '08b')
        binary_imm_lower = format(imm_lower, '06b')
        return binary_imm_upper, rs2, rs1, funct3_list[parts2[0]], binary_imm_lower, opcode

input_file = r"C:\Users\Suvit Joshia\Downloads\CO Project evaluation framework\CO Project evaluation framework\automatedTesting\tests\assembly\simpleBin\test2.txt"
output_file = r"output2.txt"

with open(input_file, "r") as f:
    assembly_code = f.readlines()

binary_instructions = []
for inst in assembly_code:
    binary_instructions.append(" ".join(assembler(inst.strip())))

with open(output_file, "w") as f:
    f.write("\n".join(binary_instructions))

print("Binary code has been written to", output_file)
