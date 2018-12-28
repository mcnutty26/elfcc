import sys

if len(sys.argv) != 3:
    print("Program takes a single argument (the input elf file)")
    sys.exit(1)

program = []
profiling = int(sys.argv[2])

with open(sys.argv[1]) as f:
    for line in f: program.append(line.strip('\n').split(' '))

if program[0][0] == "#ip":
    ip_r = int(program.pop(0)[1])
else:
    ip_r = 6

start = """
#include <stdio.h>

int addr(int a, int b){return a + b;}
int addi(int a, int b){return a + b;}
int mulr(int a, int b){return a * b;}
int muli(int a, int b){return a * b;}
int banr(int a, int b){return a & b;}
int bani(int a, int b){return a & b;}
int borr(int a, int b){return a | b;}
int bori(int a, int b){return a | b;}
int setr(int a, int b){return a;}
int seti(int a, int b){return a;}
int gtir(int a, int b){return a > b;}
int gtri(int a, int b){return a > b;}
int gtrr(int a, int b){return a > b;}
int eqir(int a, int b){return a == b;}
int eqri(int a, int b){return a == b;}
int eqrr(int a, int b){return a == b;}
"""

main = """
int main()
{

    struct operation{
        int o;
        int a;
        int b;
        int c;
    };
    
    int ip = 0;
    int r[7] = {0,0,0,0,0,0,0};
    int (*opcodes[16])(int x, int y) = {addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr};
    char* strcodes[16] = {"addr","addi","mulr","muli","banr","bani","borr","bori","setr","seti","gtir","gtri","gtrr","eqir","eqri","eqrr"};
"""

end1 = """
    printf("[%d, %d, %d, %d, %d, %d]\\n",r[0], r[1], r[2], r[3], r[4], r[5]);
    return 0;
}
"""

end2 = """
    printf("[%d, %d, %d, %d, %d, %d]\\n",r[0], r[1], r[2], r[3], r[4], r[5]);
    printf("\\nPROFILING RESULTS:\\n=================\\n");
    for (int i = 0; i < len; i++){
        printf("line %d: ", i);
        if (i < 10){printf(" ");}
        if (i < 100){printf(" ");}
        printf("%d\\t", heat[i]);
        if (heat[i] < 100000){printf("\\t");}
        printf("(%s %d %d %d)\\n", strcodes[ops[i].o], ops[i].a, ops[i].b, ops[i].c);
    }
    return 0;
}
"""

loop1 = """
    do {
"""
loop2 = f"""
        r[{ip_r}] = ip;
        if (ops[ip].o==0||ops[ip].o==2||ops[ip].o==4||ops[ip].o==6||ops[ip].o==8||ops[ip].o==12||ops[ip].o==15){{
            r[ops[ip].c] = (*opcodes[ops[ip].o])(r[ops[ip].a], r[ops[ip].b]);
        }}
        else if (ops[ip].o==1||ops[ip].o==3||ops[ip].o==5||ops[ip].o==7||ops[ip].o==11||ops[ip].o==14){{
            r[ops[ip].c] = (*opcodes[ops[ip].o])(r[ops[ip].a], ops[ip].b);
        }}
        else {{
            r[ops[ip].c] = (*opcodes[ops[ip].o])(ops[ip].a, r[ops[ip].b]);
        }}
        ip = r[{ip_r}];
        ip++;
    }} while (ip > 0 && ip < len);"""

ops = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

print(start)
print(f"const int len = {len(program)};")
if profiling:
    print("int heat[len];")
    print("void profile(int i){heat[i]++;}")
else: print("void profile(int i){}")
print(main)
print(f"    struct operation ops[len];")

for i in range(len(program)):
    print(f"    ops[{i}].o = {ops.index(program[i][0])};")
    print(f"    ops[{i}].a = {program[i][1]};")
    print(f"    ops[{i}].b = {program[i][2]};")
    print(f"    ops[{i}].c = {program[i][3]};")

print(loop1)
if profiling: print("        profile(ip);")
print(loop2)
if profiling: print(end2)
else: print(end1)
