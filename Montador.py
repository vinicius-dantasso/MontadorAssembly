##########################################################
#Equipe: FRANCISCO NÍCOLAS FERNANDES BARRÊTO             #
#        VINICIUS DANTAS DE SOUSA                        #
##########################################################

import re

#Inicializando os valores das tabelas 
opCode = (0,2,3,4,5,8,9,10,11,12,13,15,28,35,43)
funct = (0,2,8,16,18,24,25,26,27,32,33,34,35,36,37,42,43)

#Váriáveis utilizadas para ler/escrever o arquivo
lines = ""
labelCount = []
currentLine = 0
saveLabel = []
num = []
cont = 0
binaryValue = 0
binary = []

###############################################
fileName = input("Insira o nome do arquivo: ")# Inserção do Nome do Arquivo
###############################################

#Adiciona todos os zeros que faltarem
def format32(bin):
    l = len(bin)
    r = 32 - l
    return ("0"*r)+bin
#Configura corretamente os números negativos em binário
def formatNegative(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)
#Função Tabela R
def tabelaR(opcode,value,funct):
    binaryValue = bin((opcode << 26 | int(value[1]) << 21 | int(value[2]) << 16 | int(value[0]) << 11 | 0 << 6 | funct))
    binaryValue = format32(binaryValue[2:])
    return binaryValue
#Função Tabela I
def tabelaI(opcode,value):
    if(value.__len__() == 3):
        binaryValue = bin((opcode << 26 | value[1] << 21 | value[0] << 16 | value[2]))
        binaryValue = format32(binaryValue[2:])
        return binaryValue
    elif(value.__len__() < 3):
        i=0
        for label in saveLabel:
            i+=1
            if(line.__contains__(label)):
                i-=1
                adress = labelCount[i] - (currentLine + 1)
                adress = formatNegative(adress, 16)
                binaryValue = bin((opcode << 26 | num[1] << 21 | num[0] << 16))
                binaryValue = binaryValue[2:15] + adress
                binaryValue = format32(binaryValue)
                return binaryValue
#Função Tabela J
def tabelaJ(opcode):
    i=0
    for label in saveLabel:
        i+=1
        if(line.__contains__(label)):
            i-=1
            if(labelCount[i] != 1):
                adress = 1048576  + (labelCount[i] - 1)
                binaryValue = bin((opcode << 26 | adress))
                binaryValue = format32(binaryValue[2:])
            else:
                adress = 1048576
                binaryValue = bin((opcode << 26 | adress))
                binaryValue = format32(binaryValue[2:])
            return binaryValue

#Leitura do arquivo .asm
fileAsm = open(fileName)
#Primeira Leitura para conferir os Labels
for line in fileAsm:
    cont += 1
    separatedLine = re.split(', |:|\$|\n|\t', line)
    while('' in separatedLine):
        separatedLine.remove('')
    
    #Confere se a linha possui um Label e salva sua posição junto do seu nome
    if(line.__contains__(':')):
        labelCount.append(cont)
        saveLabel.append(separatedLine[0])

fileAsm.close()

#Segunda Leitura do arquivo .asm e criação do arquivo .bin
fileBin = open(fileName.replace(".asm",".bin"), 'w')
fileAsm = open(fileName)           

for line in fileAsm:
    currentLine += 1
    separatedLine = re.split(',| ,|:|\$|\(|\)|\n|\t', line)

    #Verificações necessárias para evitar conflitos
    if(line.__contains__("addiu")): #Tabela I
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[6], num))
        num.clear()
    elif(line.__contains__("addi")): #Tabela I
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[5], num))
        num.clear()
    elif(line.__contains__("addu")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaR(opCode[0], num, funct[10]))
        num.clear()
    elif(line.__contains__("add")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[9]))
        num.clear()


    if(line.__contains__("multu")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | int(num[0]) << 21 | int(num[1]) << 16 | 0 << 11 | 0 << 6 | funct[6]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("mult")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | int(num[0]) << 21 | int(num[1]) << 16 | 0 << 11 | 0 << 6 | funct[5]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("mul")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[12], num, funct[1]))
        num.clear()


    if(line.__contains__("subu")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[12]))
        num.clear()
    elif(line.__contains__("sub")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[11]))
        num.clear()


    if(line.__contains__("divu")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | int(num[0]) << 21 | int(num[1]) << 16 | 0 << 11 | 0 << 6 | funct[8]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("div")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | int(num[0]) << 21 | int(num[1]) << 16 | 0 << 11 | 0 << 6 | funct[7]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()


    if(line.__contains__("sltu")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[16]))
        num.clear()
    elif(line.__contains__("slti")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[7], num))
        num.clear()
    elif(line.__contains__("slt")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[15]))
        num.clear()


    if(line.__contains__("andi")): #Tabela I
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[9], num))
        num.clear()
    elif(line.__contains__("and")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[13]))
        num.clear()
    

    if(line.__contains__("ori")): #Tabela I
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[10], num))
        num.clear()
    elif(line.__contains__("or")): #Tabela R
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binary.append(tabelaR(opCode[0], num, funct[14]))
        num.clear()

    ################################

    #Conferir se está na Tabela R
    if(line.__contains__("sll")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | 0 << 21 | int(num[1]) << 16 | int(num[0]) << 11 | int(num[2]) << 6 | funct[0]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("srl")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | 0 << 21 | int(num[1]) << 16 | int(num[0]) << 11 | int(num[2]) << 6 | funct[1]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("jr")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | int(num[0]) << 21 | 0 << 16 | 0 << 11 | 0 << 6 | funct[2]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
        continue
    elif(line.__contains__("mfhi")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | 0 << 21 | 0 << 16 | int(num[0]) << 11 | 0 << 6 | funct[3]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    elif(line.__contains__("mflo")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(item)
        binaryValue = bin((opCode[0] << 26 | 0 << 21 | 0 << 16 | int(num[0]) << 11 | 0 << 6 | funct[4]))
        binaryValue = format32(binaryValue[2:])
        binary.append(binaryValue)
        num.clear()
    
    #######################################

    #Conferir se está na Tabela I
    if(line.__contains__("beq")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))

        if(num.__len__() == 3):
            binaryValue = bin((opCode[3] << 26 | num[0] << 21 | num[1] << 16 | num[2]))
            binaryValue = format32(binaryValue[2:])
        elif(num.__len__() < 3):
            i=0
            for label in saveLabel:
                i+=1
                if(line.__contains__(label)):
                    i-=1
                    adress = labelCount[i] - (currentLine + 1)
                    adress = formatNegative(adress, 16)
                    binaryValue = bin((opCode[3] << 26 | num[0] << 21 | num[1] << 16))
                    binaryValue = binaryValue[2:15] + adress
                    binaryValue = format32(binaryValue)
                    break
            binary.append(binaryValue)
            num.clear()
    elif(line.__contains__("bne")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))

        if(num.__len__() == 3):
            binaryValue = bin((opCode[4] << 26 | num[0] << 21 | num[1] << 16 | num[2]))
            binaryValue = format32(binaryValue[2:])
        elif(num.__len__() < 3):
            i=0
            for label in saveLabel:
                i+=1
                if(line.__contains__(label)):
                    i-=1
                    adress = labelCount[i] - (currentLine + 1)
                    adress = formatNegative(adress, 16)
                    binaryValue = bin((opCode[4] << 26 | num[0] << 21 | num[1] << 16))
                    binaryValue = binaryValue[2:15] + adress
                    binaryValue = format32(binaryValue)
                    break
            binary.append(binaryValue)
            num.clear()
    elif(line.__contains__("sltiu")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
        binary.append(tabelaI(opCode[8], num))
        num.clear()
    elif(line.__contains__("lui")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
            
        if(num.__len__() == 2):
            binaryValue = bin((opCode[11] << 26 | 0 << 21 | num[0] << 16 | num[1]))
            binaryValue = format32(binaryValue[2:])
            binary.append(binaryValue)
            num.clear()
        elif(num.__len__() < 2):
            i=0
            for label in saveLabel:
                i+=1
                if(line.__contains__(label)):
                    i-=1
                    binaryValue = bin((opCode[11] << 26 | 0 << 21 | num[0] << 16 | labelCount[i]))
                    binaryValue = format32(binaryValue[2:])
                    binary.append(binaryValue)
                    num.clear()
    elif(line.__contains__("lw")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
            
        if(num.__len__() == 3):
            binaryValue = bin((opCode[13] << 26 | num[2] << 21 | num[0] << 16 | num[1]))
            binaryValue = format32(binaryValue[2:])
            binary.append(binaryValue)
            num.clear()
        elif(num.__len__() < 3):
            i=0
            for label in saveLabel:
                i+=1
                if(line.__contains__(label)):
                    i-=1
                    binaryValue = bin((opCode[13] << 26 | num[1] << 21 | num[0] << 16 | labelCount[i]))
                    binaryValue = format32(binaryValue[2:])
                    binary.append(binaryValue)
                    num.clear()
    elif(line.__contains__("sw")):
        for item in separatedLine:
            if(item.isdigit()):
                num.append(int(item))
            
        if(num.__len__() == 3):
            binaryValue = bin((opCode[14] << 26 | num[2] << 21 | num[0] << 16 | num[1]))
            binaryValue = format32(binaryValue[2:])
            binary.append(binaryValue)
            num.clear()
        elif(num.__len__() < 3):
            i=0
            for label in saveLabel:
                i+=1
                if(line.__contains__(label)):
                    i-=1
                    binaryValue = bin((opCode[14] << 26 | num[1] << 21 | num[0] << 16 | labelCount[i]))
                    binaryValue = format32(binaryValue[2:])
                    binary.append(binaryValue)
                    num.clear()


    #Conferir se está na Tabela J
    if(line.__contains__("jal")):
        binary.append(tabelaJ(opCode[2]))
    elif(line.__contains__('j')):
        binary.append(tabelaJ(opCode[1]))


for line in binary:
    fileBin.write(line + '\n')

fileBin.close()