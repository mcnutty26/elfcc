import sys

if len(sys.argv) != 3:
    print("Program takes two arguments (the input elf file and 1/0 to enable/disable profiling)")
    sys.exit(1)

program = []
PROFILING = int(sys.argv[2])
IPBIND = False

with open(sys.argv[1]) as f:
    for line in f: program.append(line.strip('\n').split(' '))

if program[0][0] == "#ip":
    ip_r = int(program.pop(0)[1])
    IPBIND = True

ops = {"addr": '+', "addi": '+', "mulr": '*', "muli": '*', "banr": '&', "bani": '&', "borr": '|', "bori": '|', "setr": '', "seti": '', "gtir": '>', "gtri": '>', "gtrr": '>', "eqir": '==', "eqri": '==', "eqrr": '=='}
regs = ["a", "b", "c", "d", "e", "f"]

print(f"IP bound register is {regs[ip_r]}")

#opt1 => transform to labels
for i in range(len(program)):
    ins = program[i]
    ins[3] = regs[int(ins[3])]
    if ins[0] in ["addr", "mulr", "banr", "borr", "gtrr", "eqrr"]:
        ins[1] = regs[int(ins[1])]
        ins[2] = regs[int(ins[2])]
    elif ins[0] in ["addi", "muli", "bani", "bori", "gtri", "eqri"]:
        ins[1] = regs[int(ins[1])]
    elif ins[0] in ["setr", "gtir", "eqir"]:
        ins[2] = regs[int(ins[1])]
    if ins[0] in ["setr", "seti"]:
        ins[1] = ""
    program[i] = [ins[3], "=", ins[1], ops[ins[0]], ins[2], ";"]
    for item in program[i]:
        if item == "": program[i].remove(item)
    for item in program[i]:
        if item == "": program[i].remove(item)

#opt2 => transform to +=/++
for i in range(len(program)):
    ins = program[i]
    if ins[3] == "+":
        if ins[2] == ins[0]:
            ins[1] = "+="
            ins[2] = ins[4]
            ins.remove("+")
            ins[3] = ""
        elif ins[4] == ins[0]:
            ins[1] = "+="
            ins.remove("+")
            ins[3] = ""
    for item in program[i]:
        if item == "": program[i].remove(item)

#opt3 => transform to gotos
for i in range(len(program)):
    ins = program[i]
    if ins[0] == regs[ip_r] and ins[1] == "=" and ins[2] not in regs:
        ins[0] = "goto"
        ins[1] = str(int(ins[2])+1)
        ins[2] = ""
    if ins[0] == regs[ip_r] and ins[1] == "+=" and ins[2] not in regs:
        ins[0] = "goto"
        ins[1] = str(int(ins[2])+1+i)
        ins[2] = ""
    elif ins[0] == regs[ip_r] and ins[1] == "+=" and (program[i-1][3] == ">" or program[i-1][3] == "=="):
        pass
    for item in program[i]:
        if item == "": program[i].remove(item)

#introduce line labels
for i in range(len(program)):
    program[i].insert(0, f"{i}:")
    print(program[i])
