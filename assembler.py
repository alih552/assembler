import sys
code = open('input.txt', 'r').readlines()
out_symbol_table = open('out_symbol_table.txt', 'w')
out_symbol_table_HEXA = open('out_symbol_table_HEXA.txt', 'w')
out_symbol_table_BIN = open('out_symbol_table_BIN.txt', 'w')
out_symbol_table_total = open('out_symbol_table_total.txt', 'w')
out_symbol_table_total.write("Symbol  |  HEX  |  BIN"+'\n'+'-------------------------'+'\n')
output = open('output.txt', 'w')

LC = 0
n = 0
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
           'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ',']
hexa_letters = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '50',
                '51', '52', '53', '54', '55', '56', '57', '58', '59', '5A', '2C']

MRI = ['AND', 'ADD', 'LDA', 'STA', 'BUN', 'BSA', 'ISZ']
MRI_opcode_i = ['0', '1', '2', '3', '4', '5', '6']
MRI_opcode_I = ['8', '9', 'A', 'B', 'C', 'D', 'E']

NON_MRI = ['CLA', 'CLE', 'CMA', 'CME', 'CIR', 'CIL', 'INC', 'SPA', 'SNA', 'SZA', 'SZE', 'HLT', 'INP', 'OUT', 'SKI',
           'SKO', 'ION', 'IOF']
NON_MRI_opcode = ['7800', '7400', '7200', '7100', '7080', '7040', '7020', '7010', '7008', '7004', '7002', '7001',
                  'F800', 'F400', 'F200', 'F100', 'F080', 'F040']


def second_pass():
    for line in code:
        word = line.split()
        if 'ORG' in line:
            LC = int(line[4:]) - 1
        elif 'END' in line:
            print("second pass finished successfully, go ahead and open 'output.txt' to find the final output")
            output.write("("+LC+") "+line)
        elif line[:3] in MRI:
            # getting the address
            LC = int(LC)
            LC +=1
            LC = str(LC)
            HEX2BIN = bin(int(LC, 16)).split('b')[-1]

            if len(HEX2BIN) < 12:
                HEX2BIN = ''.join(('000', HEX2BIN))
            HEX2BIN = " ".join(HEX2BIN[i:i + 4] for i in range(0, len(HEX2BIN), 4))

            # check if direct or indirect and getting the opcode
            if '[' in line:
                opcodeIndirect = MRI_opcode_I[MRI.index(line[:3])]
                HEX2BIN2 = bin(int(opcodeIndirect, 16)).split('b')[-1]
                output.write(line+"(" + LC + ") "+HEX2BIN2+' '+HEX2BIN+'\n')
            else:
                opcodeDirect = MRI_opcode_i[MRI.index(line[:3])]
                HEX2BIN2 = bin(int(opcodeDirect, 16)).split('b')[-1]
                if len(HEX2BIN2) == 1:
                    HEX2BIN2 = ''.join(('000', HEX2BIN2))
                elif len(HEX2BIN2) == 2:
                    HEX2BIN2 = ''.join(('00', HEX2BIN2))
                elif len(HEX2BIN2) == 3:
                    HEX2BIN2 = ''.join(('0', HEX2BIN2))
                output.write(line+"("+LC+") "+HEX2BIN2+' '+HEX2BIN+'\n')
        elif line[:3] in NON_MRI:
            # getting the address
            LC = int(LC)
            LC += 1
            LC = str(LC)
            HEX2BIN = bin(int(LC, 16)).split('b')[-1]
            if len(HEX2BIN) < 12:
                HEX2BIN = ''.join(('000', HEX2BIN))
            HEX2BIN = " ".join(HEX2BIN[i:i + 4] for i in range(0, len(HEX2BIN), 4))
            opcodeNON_MRI = NON_MRI_opcode[NON_MRI.index(line[:3])]
            HEX2BIN2 = bin(int(opcodeNON_MRI, 16)).split('b')[-1]
            if len(HEX2BIN2) == 15:
                HEX2BIN2 = ''.join((HEX2BIN2, '0'))
            HEX2BIN2 = " ".join(HEX2BIN2[i:i + 4] for i in range(0, len(HEX2BIN2), 4))
            output.write(line+"("+LC+") "+HEX2BIN2+'\n')
        elif ',' in line:
            # getting the address
            LC = int(LC)
            LC += 1
            LC = str(LC)
            HEX2BIN = bin(int(LC, 16)).split('b')[-1]
            if len(HEX2BIN) < 12:
                HEX2BIN = ''.join(('000', HEX2BIN))
            HEX2BIN = " ".join(HEX2BIN[i:i + 4] for i in range(0, len(HEX2BIN), 4))
            output.write(line+"("+LC+") "+HEX2BIN+'\n')
        else:
            print("Error: check your syntax")
            sys.exit(True)



for line in code:
    word = line.split()
    for i in word:
        # scanning for Label
        if ',' in i:
            out_symbol_table.write(i[0:2]+'\n'+i[2:4]+'\n')
            for letter in list(i):
                # get each letter in the list
                if letter in letters:
                    # check the letter existence and convert it to binary
                    index = letters.index(letter)
                    HEXA2BIN = bin(int(hexa_letters[index], 16))
                    HEXA2BIN = HEXA2BIN.replace('b', '')
                    HEXA2BIN = " ".join(HEXA2BIN[i:i+4] for i in range(0, len(HEXA2BIN), 4))
                    HEXA2BIN = HEXA2BIN.split(' ')
                    if len(HEXA2BIN[0]) == 3:
                        HEXA2BIN[0] = ''.join(('0', HEXA2BIN[0]))
                    elif len(HEXA2BIN[1]) == 3:
                        HEXA2BIN[0] = ''.join(('0', HEXA2BIN[0]))
                    else: pass
                    # write output to files
                    out_symbol_table_HEXA.write(hexa_letters[index]+'\n')
                    out_symbol_table_BIN.write(HEXA2BIN[0] + HEXA2BIN[1] + '\n')
                    n += 1
                    # Increment LC and save it in the HEX table and BIN table
                    if n == 4:
                        LC += 1
                        LC = str(LC)
                        if len(LC) == 3:
                            LC = ''.join(('0', LC))
                        else: pass
                        HEX2BIN = bin(int(LC, 16)).split('b')[-1]
                        if len(HEX2BIN) < 16:
                            HEX2BIN = ''.join(('0000000', HEX2BIN))
                        HEX2BIN = " ".join(HEX2BIN[i:i + 8] for i in range(0, len(HEX2BIN), 8))
                        HEX2BIN = HEX2BIN.split(' ')
                        out_symbol_table_BIN.write(HEX2BIN[0] + '\n'+HEX2BIN[1] + '\n')
                        LC = " ".join(LC[i:i + 2] for i in range(0, len(LC), 2))
                        LC = LC.split(' ')
                        DEC2HEXA = hex(int(LC[0])).split('x')[-1]
                        if len(DEC2HEXA) == 1:
                            DEC2HEXA = ''.join(('0', DEC2HEXA))
                        else: pass
                        out_symbol_table_HEXA.write(DEC2HEXA + '\n')
                        DEC2HEXA = hex(int(LC[1])).split('x')[-1]
                        if len(DEC2HEXA) == 1:
                            DEC2HEXA = ''.join(('0', DEC2HEXA))
                        else:
                            pass
                        LC = "".join(LC)
                        out_symbol_table_HEXA.write(DEC2HEXA + '\n')
                        out_symbol_table_total.write("  (LC)    " + LC + '\n')
                        LC = int(LC)
                        n = 0
                    out_symbol_table_total.write('   '+letter+'       '+hexa_letters[index]+'    '+
                                                 HEXA2BIN[0]+HEXA2BIN[1]+'\n')
                else:
                    print("Error: check your syntax")
                    sys.exit(True)
    # scanning for ORG
    if 'ORG' in line:
        LC = int(line[4:]) - 1
    elif 'END' in line:
        print("The first pass finished successfully, go ahead and open 'out_symbol_table_total.txt' to find the "
              "results of the first pass")
        second_pass()
    # scanning for instructions to set LC
    elif "," not in line:
        LC += 1

