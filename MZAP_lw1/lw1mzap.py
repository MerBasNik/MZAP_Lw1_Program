Data = open('data.txt')
codes = []
Codes = open('codes.txt')
for i in range(124):
    codes.append(Codes.readline().split('----'))
    codes[i][0] = codes[i][0].split(' ')
    if codes[i][0][0] == '*jmp':
        codes[i][0][0] = 'jmp'
    if codes[i][0][0] == '*call':
        codes[i][0][0] = 'call'


def findCom(com):
    mas = []
    int_com = int(com[0], 16)
    for i in range(len(codes)):
        if com[1] == codes[i][1]:
            mas.append([codes[i][0], com[1], codes[i][1]])
            break

    if len(mas) == 0:
        for i in range(len(codes)):
            if com[1][0:4] == codes[i][1][0:4] and (0 < len(codes[i][1]) - len(com[1]) <= 8):
                mask_and = int(codes[i][2], 2)
                mask_xor = int(codes[i][3], 2)
                if (int_com ^ mask_xor) & mask_and == 0:
                    mas.append([codes[i][0], com[1], codes[i][1]])

    if len(mas) == 0:
        for i in range(len(codes)):
            if com[1][0:4] == codes[i][1][0:4] and (0 < len(codes[i][1]) - len(com[1]) <= 8):
                mas.append([codes[i][0], com[1], codes[i][1]])
                break

    if len(mas) >= 2:
        max_s = 0
        temp_mas = []
        for i in range(len(mas) - 1):
            k = 0
            s = 0
            for j in range(len(mas[i][2]) - 1):
                if mas[i][1][k] == mas[i][2][j]:
                    s += 1
                if mas[i][2][j] != ' ':
                    k += 1
            if s > max_s:
                if len(temp_mas) != 0:
                    mas.remove(temp_mas)
                temp_mas = mas[i]
                max_s = s
    if len(mas) >= 2:
        temp_mas = []
        for i in range(len(mas)):
            if 'K' in mas[i][2] or 'r' in mas[i][2]:
                temp_mas = mas[i]
        if len(temp_mas) == 0:
            for i in range(len(mas)):
                if len(mas[i][0][1].split(',')) == 1:
                    temp_mas = mas[i]
        mas = [temp_mas]
    return mas


def getNumStr(n, f):
    n = int(n, 16)
    if f == 1:
        n += 4
    else:
        n += 2
    return hex(n)[2:].zfill(2)


def getK(command):
    reg1 = reg2 = ''
    if len(command[0]) == 2:
        if len(command[0][1].split(',')) == 2:
            reg1, reg2 = command[0][1].split(',')
            if len(reg1) == 1 and reg1 in 'sPk':
                reg1 = reg1[0]
            elif (len(reg1) == 2 and not ('X' in reg1) and not ('Y' in reg1) and not ('Z' in reg1)) or (
                    len(reg1) == 3 and not ('+' in reg1)):
                reg1 = reg1[1]
            elif len(reg1) == 3 and '+' in reg1:
                reg1 = reg1[2]
            else:
                reg1 = reg2

            if len(reg2) == 1 and reg2 in 'bsPkK':
                reg2 = reg2[0]
            elif (len(reg2) == 2 and not ('X' in reg2) and not ('Y' in reg2) and not ('Z' in reg2)) or (
                    len(reg2) == 3 and not ('+' in reg2)):
                reg2 = reg2[1]
            elif len(reg2) == 3 and '+' in reg2:
                reg2 = reg2[2]
        else:
            reg1 = command[0][1]
            if (len(reg1) == 2 and not ('X' in reg1) and not ('Y' in reg1) and not ('Z' in reg1)) or (
                    len(reg1) == 3 and not ('+' in reg1)):
                reg1 = reg1[1]
        bin_cod = command[1]
        mask_com = command[2]
        i = 0
        r1 = r2 = ''
        for j in range(len(mask_com)):
            if reg1 != '' and mask_com[j] in reg1:
                r1 += bin_cod[i]
            if reg2 != '' and mask_com[j] in reg2:
                r2 += bin_cod[i]
            if not (mask_com[j] in ' '):
                i += 1
        return [r1, r2, reg1, reg2]
    else:
        return ['nil', 'nil', reg1, reg2]


def reverseNum(n):
    r = ''
    for i in range(len(n)):
        if n[i] == '1':
            r += '0'
        else:
            r += '1'
    return r


def getValue(command):
    val = []
    bin_cod = command[1]
    m = getK(command)
    r1 = m[0]
    r2 = m[1]
    reg1 = m[2]
    reg2 = m[3]
    if command[0][0] == 'jmp' or command[0][0] == 'call':
        bin_cod = int(bin_cod[-8:], 2)
        val = [hex(bin_cod << 1), hex(bin_cod << 1)]
    elif command[0][0] == 'subi' or command[0][0] == 'ldi' or command[0][0] == 'sbci':
        d = 'r' + str(int(r1, 2) + 16)
        k = hex(int(r2, 2))
        val = [d + ', ' + k, int(k[2:], 16)]
    elif r1 == 'nil':
        val = ['', '']
    elif r1 != '' and r2 != '':
        comment = int(r1, 2)
        if reg1 == 'r' or command[0][0] == 'eor' or command[0][0] == 'ldi' or command[0][0] == 'sbci':
            r1 = 'r' + str(int(r1, 2))
        else:
            r1 = hex(int(r1, 2))
        if reg2 == 'r' or command[0][0] == 'eor':
            r2 = 'r' + str(int(r2, 2))
        else:
            r2 = hex(int(r2, 2))
        val = [r1 + ', ' + r2, comment]
    elif r1[0] == '1':
        int_k = int(reverseNum(r1), 2) + 1
        k = int_k << 1
        val = [-k, '']
    elif r1[0] == '0':
        int_k = int(r1, 2)
        k = int_k << 1
        val = [k, '']
    return val


num_str = '0'
for Q in range(12):
    hex_commands = []
    data_str = Data.readline()
    str_hex = []
    str_hex.append(data_str[0:3])
    str_hex.append(data_str[3:7])
    str_hex.append(data_str[7:9])
    if data_str[-2:] != 'FF':
        j = 9
        for i in range((len(data_str) - 11) // 4):
            str_hex.append(data_str[j:j + 4])
            j += 4
        str_hex.append(data_str[-3:])
        for i in range(3, len(str_hex) - 1):
            str_hex[i] = str_hex[i][2:4] + str_hex[i][0:2]
        f = 0
        for i in range(3, len(str_hex) - 1):
            if f == 1:
                f = 0
                continue
            elif str_hex[i][0:2] == '94' and '0' in str_hex[i]:
                r = str_hex[i] + str_hex[i + 1]
                f = 1
                hex_commands.append([r, bin(int(r, 16))[2:]])
            else:
                hex_commands.append([str_hex[i], bin(int(str_hex[i], 16))[2:].zfill(16)])

        for i in range(len(hex_commands)):
            com = findCom(hex_commands[i])[0]
            val = getValue(com)
            input_hex_com = hex_commands[i][0][2:4] + ' ' + hex_commands[i][0][0:2]
            if len(hex_commands[i][0]) == 8:
                input_hex_com = input_hex_com + ' ' + hex_commands[i][0][6:] + ' ' + hex_commands[i][0][4:6]
            input_com = com[0][0]
            print(str(num_str) + ': ' + input_hex_com + ' ' + input_com + ' ' + str(val[0]) + ' ; ' + str(val[1]))
            if len(com[2]) > 30:
                num_str = getNumStr(num_str, 1)
            else:
                num_str = getNumStr(num_str, 0)
