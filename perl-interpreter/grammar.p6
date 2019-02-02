my $input = "#ip 0; addi 5 3 4; mulr 1 2 3;";

grammar elf-definition {

	rule TOP {
		[<instruction-pointer> ';']? [\s* <operation> ';']+
	}

	rule instruction-pointer {
		"#ip" <register>
	}

	token register {
		<[0..5]>**1
	}

	rule  operation {
		<opcode> <register> <register> <register>
	}

	token opcode {
		| addr
		| addi
		| mulr
		| muli
	}

	token addr { "addr" }
	token addi { "addi" }
	token mulr { "mulr" }
	token muli { "muli" }
	token banr { "banr" }
	token bani { "bani" }
	token borr { "borr" }
	token bori { "bori" }
	token setr { "setr" }
	token seti { "seti" }
	token gtir { "gtir" }
	token gtri { "gtri" }
	token gtrr { "gtrr" }
	token eqir { "eqir" }
	token eqri { "eqri" }
	token eqrr { "eqrr" }

}

class elf-grammar {
	method generate-ast($program) {
		return elf-definition.parse($program);
	}
}

say elf-grammar.generate-ast($input)
