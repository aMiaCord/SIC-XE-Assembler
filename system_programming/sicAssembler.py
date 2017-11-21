DEX_HEX=['A','B','C','D','E','F']
def dex_to_hex(x):
    x=int(x)
    ret=''
    if(x>=16):
        ret+=dex_to_hex(int(x/16))
    x=x%16
    if(x<10):
        ret+=str(x)
    else:
        ret+=DEX_HEX[x-10]
    return str(ret)

def parsing(ftext):
    for i in range(len(ftext)):
        ftext[i] = ftext[i].split('\t')
        ftext[i] = list(filter(lambda a: a!='',ftext[i]))
        for j in range(len(ftext[i])):
            ftext[i][j]= ftext[i][j].strip()
    return ftext


def form(n,x):
    x=str(x)
    x='0'*(n-len(x))+x
    return x

def valid(start_address,code):
    if(int('0x'+code[0],16)-int('0x'+start_address,16)>=28):
        return False
    elif(code[-2]=='RESW' or code[-2]=='RESB'):
        return False
    return True
def IsDex(ch):
    if(ch>='0' and ch<='9'):
        return True
    return False

def IsSymbol(operand):
    if(operand[0] in['#','@']):
        return False
    for ch in operand:
        if(IsDex(ch)):
            return False
    return True

def subtract_hex(a,b):
    a=int('0x'+str(a),16)
    b=int('0x'+str(b),16)
    a=a-b
    return dex_to_hex(a)
def char_to_hex(string):
    ret=''
    for ch in string:
        ret+=dex_to_hex(ord(ch))
    return ret
def append(a,b):
    ret=[]
    for i in a:
        ret.append(i)
    ret.append(b)
    #print(ret)
    return ret
def complement(dex):
    bin=binary(dex)
    comp=''
    for ch in bin:
        if(ch=='0'):
            comp+='1'
        else:
            comp+='0'
    comp=list(comp)
    for i in range(1,len(comp)+1):
        if(comp[-i]=='1'):
            comp[-i]='0'
        else:
            comp[-i]='1'
            break
    tmp=''
    for ch in comp:
        tmp+=ch
    comp=tmp
    return debinary(comp)
def binary(dex):
    ret=''
    while(dex>0):
        if(dex%2==1):
            ret='1'+ret
        else:
            ret='0'+ret
        dex=int(dex/2)
    ret='0'*(12-len(ret))+ret
    return ret
def debinary(bin):
    ret=0
    for bit in bin:
        ret*=2
        if(bit=='1'):
            ret+=1
        else:
            continue
    return ret
def hex_dex_sum(hex,dex,length):
    tmp = int('0x'+str(hex),16)+int(dex)
    if(tmp<0):
        tmp= complement(-tmp)
    tmp = dex_to_hex(tmp)
    return '0'*(length-len(tmp))+tmp

WHITE_SPACE = [' ','\t','\n']
REGISTER = {'A':0,'X':1,'L':2,'B':3,'S':4,'T':5,'F':6,'PC':8,'SW':9}
OPTAB = {'ADD':'18', 'AND':'40', 'COMP':'28', 'DIV':'24', 'J':'3C',
         'JEQ':'30', 'JGT':'34', 'JLT':'38', 'JSUB':'48', 'LDA':'00',
         'LDCH':'50', 'LDL':'08', 'LDX':'04', 'MUL':'20', 'OR':'44',
         'RD':'D8', 'RSUB':'4C', 'STA':'0C', 'STCH':'54', 'STL':'14',
         'STSW':'E8', 'STX':'10', 'SUB':'1C', 'TD':'E0', 'TIX':'2C', 'WD':'DC'}
OPTAB_XE_format1 = {'FIX':'C4','FLOAT':'C0','HIO':'F4','NORM':'C8',
                    'SIO':'F0','TIO':'F8'}
OPTAB_XE_format2 = {'ADDR':'90','CLEAR':'B4','COMPR':'A0','DIVR':'9C',
                    'MULR':'98','RMO':'AC','SHIFTL':'A4','SHIFTR':'A8',
                    'SUBR':'94','SVC':'B0','TIXR':'B8'}
OPTAB_XE_format3 = {'ADDF':'58','COMPF':'88','DIVF':'64','LDB':'68',
                    'LDF':'70','LDS':'6C','LDT':'74','LPS':'D0',
                    'MULF':'60','SSK':'EC','STB':'78','STF':'80',
                    'STI':'D4','STS':'7C','STT':'84','SUBF':'5C'}
OPTAB_XE_format3.update(OPTAB)
file = open('SPHW1_XE.txt','r')
ftext = parsing(file.readlines())
LOCCTR=0
SYMTAB={}

#pass 1
def pass1():

    intermediate=[]
    for line in ftext:
        if(line[0]=='RSUB'):
            intermediate.append(str(dex_to_hex(LOCCTR)) + '\t'*(4-len(line)) + '\t'.join(line))
            LOCCTR+=3
        elif(line[0]=='.'):
            continue
        elif(line[1]=='START'):
            SYMTAB[line[0]]=line[2]
            prog_name=line[0]
            LOCCTR=int('0x'+line[2],16)
            intermediate.append(str(dex_to_hex(LOCCTR)) + '\t'*(4-len(line)) + '\t'.join(line))
        elif(line[0]=='BASE'):
            intermediate.append('\t'*(4-len(line)) + '\t'.join(line))
        elif(line[0]!='END'):
            if(line[0]!='.'):
                if(len(line)==3):
                    if(line[0] in SYMTAB.keys()):
                        print("ERROR! Already set symbol")
                    else:
                        SYMTAB[line[0]]=dex_to_hex(LOCCTR)
                intermediate.append(str(dex_to_hex(LOCCTR)) + '\t'*(4-len(line)) + '\t'.join(line))
                if(line[-2] == 'WORD'):
                    LOCCTR+=3
                elif(line[-2] == 'RESW'):
                    LOCCTR+=3*int(line[2])
                elif(line[-2] == 'RESB'):
                    LOCCTR+=int(line[2])
                elif(line[-2]=='BYTE'):
                    if(line[-1][0]=='X'):
                        LOCCTR+=int(len(line[-1][2:-1]))/2
                    elif(line[-1][0]=='C'):
                        LOCCTR+=int(len(line[-1][2:-1]))
                elif(len(line)==2):
                    if(line[0] in OPTAB_XE_format3.keys()):
                        LOCCTR+=3
                    elif(line[0] in OPTAB_XE_format1.keys()):
                        LOCCTR+=1
                    elif(line[0] in OPTAB_XE_format2.keys()):
                        LOCCTR+=2
                    elif(line[0][0]=='+'):
                        if(line[0][1:] in OPTAB_XE_format3.keys()):
                            LOCCTR+=4
                        else:
                            print("ERROR! Undefined operate tried to excute at line : " + str(line))
                    else:
                        print("ERROR! Undefined operate tried to excute at line : " + str(line))
                elif(len(line)==3):
                    if(line[1] in OPTAB_XE_format3.keys()):
                        LOCCTR+=3
                    elif(line[1] in OPTAB_XE_format1.keys()):
                        LOCCTR+=1
                    elif(line[1] in OPTAB_XE_format2.keys()):
                        LOCCTR+=2
                    elif(line[1][0]=='+'):
                        if(line[1][1:] in OPTAB_XE_format3.keys()):
                            LOCCTR+=4
                        else:
                            print("ERROR! Undefined operate tried to excute at line : " + str(line))
                    else:
                        print("ERROR! Undefined operate tried to excute at line : " + str(line))

                else:
                    print("ERROR! Undefined operate tried to excute at line : " + str(line))

        else:
            intermediate.append('\t'*2+'\t'.join(line))
    #print(SYMTAB)
    intermediate='\n'.join(intermediate)
    prog_length=LOCCTR-int(SYMTAB[prog_name],16)
    print(intermediate)
    return intermediate,prog_length
    

#path 2
def pass2(intermediate,prog_length):
    intermediate = parsing(intermediate.split('\n'))
    prog_counter = 0
    listing=[]
    object_code=''
    OPpart=''
    modification_record=''
    base_address=0
    for line in intermediate:
        #Set Header
        OPline=''
        #addressing mode[0] = <n,i>, addressing mode[1] = <x,b,p,e>
        #sic => <n,i>==<0,0>
        addressing_mode=[4,16]
        if(line[-2]=='START'):
            listing.append(line)
            object_code+='H'+line[1]+'\t'+form(6,line[3])+form(6,str(dex_to_hex(prog_length)))+'\n'
            start_address=line[3]
        #make text code
        #to 수정
        elif(line[-2]=='BASE'):
            base_address=int('0x'+SYMTAB[line[-1]],16)
            continue
        elif(line[-2]!='END'):
            if(line[0]!='.'):
                #change line
                if(not valid(start_address,line)):
                    if(OPpart!=''):
                        object_code+='T'+form(6,start_address)+form(2,dex_to_hex(len(OPpart)/2))+OPpart+'\n'
                    OPpart=''
                    start_address=line[0]
                #case symbol
                if(line[1] == 'RSUB'):
                    OPline='4F0000'
                    prog_counter+=3
                #to 수정
                elif(line[-2] in OPTAB_XE_format3.keys()):
                    prog_counter+=3
                    addressing_mode=[3,2]
                    if(IsSymbol(line[-1])):
                        if(line[-1].split(',')[0] in SYMTAB.keys()):
                            if(len(line[-1].split(','))!=1):
                                addressing_mode[1]+=8
                            if(prog_counter-int('0x'+SYMTAB[line[-1].split(',')[0]],16)<int('0x1000',16)):
                                OPline=hex_dex_sum(SYMTAB[line[-1].split(',')[0]],-prog_counter,3)
                            else:
                                addressing_mode[1]+=2
                                OPline=hex_dex_sum(SYMTAB[line[-1].split(',')[0]],-base_address,3)
                        else:
                            OPline+='0000'
                            print("ERROR! Undefined symbol is used.")
                    elif(line[-1][0]=='#'):
                        addressing_mode[0]=1
                        if(IsSymbol(line[-1][1:])):
                            if(prog_counter-int('0x'+SYMTAB[line[-1][1:].split(',')[0]],16)<int('0x1000',16)):
                                addressing_mode[1]=2
                                OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],-prog_counter,3)
                            else:
                                addressing_mode[1]=4
                                OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],-base_address,3)
                        elif(IsDex(line[-1][1:])):
                            addressing_mode[1]=0
                            OPline+=hex_dex_sum(dex_to_hex(line[-1][1:]),0,3)
                    elif(line[-1][0]=='@'):
                        addressing_mode[0]=2
                        if(IsSymbol(line[-1][1:])):
                            addressing_mode[1]=2
                            OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],-prog_counter,3)
                        else:
                            print("undefined symbol used",line)
                    else:
                        OPline+='0000'
                    OPline=hex_dex_sum(OPTAB_XE_format3[line[-2]],addressing_mode[0],2) + dex_to_hex(addressing_mode[1]) + OPline
                
                elif(line[-2] in OPTAB_XE_format1.keys()):
                    prog_counter+=1
                    OPline=OPTAB_XE_format1[line[-2]]
                
                elif(line[-2] in OPTAB_XE_format2.keys()):
                    prog_counter+=2
                    if(len(line[-1].split(','))==1):
                        addressing_mode=[REGISTER[line[-1]],0]
                    elif(len(line[-1].split(','))==2):
                        addressing_mode=[REGISTER[line[-1][0]],REGISTER[line[-1][-1]]]
                    else:
                        addressing_mode=[-1,-1]
                    if(-1 in addressing_mode):
                        print("ERROR! Undefined register is used.")
                    OPline=OPTAB_XE_format2[line[-2]] + str(addressing_mode[0]) + str(addressing_mode[1])
                #to 수정
                elif(line[-2] in OPTAB_XE_format3.keys()):
                    prog_counter+=3
                    addressing_mode=[3,2]
                    if(IsSymbol(line[-1])):
                        if(line[-1].split(',')[0] in SYMTAB.keys()):
                            if(len(line[-1].split(','))!=1):
                                addressing_mode[1]+=8
                            OPline+=hex_dex_sum(SYMTAB[line[-1].split(',')[0]],-prog_counter,3)
                        else:
                            OPline+='0000'
                            print("ERROR! Undefined symbol is used.")
                    elif(line[-1][0]=='#'):
                        addressing_mode[0]=1
                        if(IsSymbol(line[-1][1:])):
                            addressing_mode[1]=2
                            OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],-prog_counter,3)
                        elif(IsDex(line[-1][1:])):
                            addressing_mode[1]=0
                            OPline+=dex_to_hex(line[-1][1:])
                    else:
                        OPline+='0000'
                    OPline=hex_dex_sum(OPTAB_XE_format3[line[-2]],addressing_mode[0],2)+dex_to_hex(addressing_mode[1])+OPline
                
                elif(line[-2][0] == '+'):
                    if(line[-2][1:] in OPTAB_XE_format3.keys()):
                        prog_counter+=4
                        addressing_mode=[3,1]
                        if(IsSymbol(line[-1])):
                            modification_record += 'M'+hex_dex_sum('0',prog_counter-3,6)+'05\n'
                            if(line[-1].split(',')[0] in SYMTAB.keys()):
                                if(len(line[-1].split(','))!=1):
                                    addressing_mode[1]+=8
                                OPline+=SYMTAB[line[-1].split(',')[0]]
                        elif(line[-1][0]=='#'):
                            addressing_mode[0]=1
                            if(IsSymbol(line[-1][1:])):
                                addressing_mode[1]+=2
                                OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],0,4)
                            elif(IsDex(line[-1][1:])):
                                addressing_mode[1]+=0
                                OPline+=hex_dex_sum(dex_to_hex(line[-1][1:]),0,4)
                        elif(line[-1][0]=='@'):
                            addressing_mode[0]=2
                            if(IsSymbol(line[-1][1:])):
                                modification_record += 'M'+hex_dex_sum('0',prog_counter-3,6)+'05\n'
                                addressing_mode[1]=2
                                OPline+=hex_dex_sum(SYMTAB[line[-1][1:]],-prog_counter,4)
                            else:
                                print("undefined symbol used",line)

                        else:
                            OPline+='0000'
                            print("ERROR! Undefined symbol is used.")
                    else:
                        OPline+='0000'
                    OPline = hex_dex_sum(OPTAB_XE_format3[line[-2][1:]],addressing_mode[0],2) + str(addressing_mode[1]) + '0'*(5-len(OPline)) + OPline

                #case [BYTE,WORD]
                elif(line[-2] == 'BYTE'):
                    if(line[-1][0]=='X'):
                        OPline+=line[-1][2:-1]
                        prog_counter+=int((len(line[-1][2:-1]))/2)
                    elif(line[-1][0]=='C'):
                        OPline+=char_to_hex(line[-1][2:-1])
                        prog_counter+=int((len(line[-1][2:-1])))
                elif(line[-2] == 'WORD'):
                    prog_counter+=3
                    OPline=form(6,dex_to_hex(line[-1]))
                elif(line[-2] in ['RESW','RESB']):
                    if(line[-2]=='RESW'):
                        prog_counter+=int(line[-1])*3
                    else:
                        prog_counter+=int(line[-1])
                    continue
                else:
                    print("Invalid line" + str(line))
                if(OPline!=''):
                    OPpart+=OPline
                #print(list(line))
                listing.append(append(line,OPline))
        else:
            if(OPpart!=''):
                object_code+='T'+form(6,start_address)+form(2,dex_to_hex(len(OPpart)/2))+OPpart+'\n'
            object_code+=modification_record
            object_code+='E'+form(6,SYMTAB[line[-1]])
            listing.append(line)
        
    #make listing line to readable
    for i in range(len(listing)):
        if(listing[i][0]=='END'):
            listing[i]=['']+listing[i]
        if(not listing[i][1] in SYMTAB.keys()):
            listing[i] = [listing[i][0]] + [''] +list(listing[i][1:])
        if(listing[i][2]=="RSUB"):
            listing[i]=listing[i][:3]+ [''] + listing[i][3:]
        if(len(listing[i][-2])<=6 and not listing[i][2] in ['START','END']):
            listing[i]= listing[i][:-1]+['']+[listing[i][-1]]
        listing[i]='\t'.join(listing[i])
    listing = '\n'.join(listing)

    print(object_code)
    return object_code
def print_OPCODE(object_code):
    file = open('SPHW1_XE-OP.txt','w')
    file.write(object_code)

intermidiate,prog_length=pass1()
object_code=pass2(intermidiate,prog_length)
print_OPCODE(object_code)