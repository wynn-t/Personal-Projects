import random
class EsoLang:
    def __init__(self, lang, tokens, instr, vars, init):
        for i in vars:
            if i in ["lang", "tokens", "instr", "vars", "init", "pntr", "code", "result", "steps", "__init__", "exit", "run", "codeInput"]:raise SyntaxError(f"cannot assign to {i}")
        self.lang, self.tokens, self.instr, self.pntr, self.vars, self.init=lang, tokens, instr, 0, vars, init
    def exit(self):pass
    def run(self, code, showInternal=False):
        print()
        for i, j in zip(self.vars, self.init):exec("self."+i+"="+j)
        self.pntr, self.code, self.result, self.steps=0, code, "", 0
        while 0<=self.pntr<len(self.code):
            token=len(self.tokens)
            for i in range(token):
                if self.tokens[i]==self.code[self.pntr:self.pntr+len(self.tokens[i])]:
                    token=i
                    break
            if token<len(self.instr):
                if self.instr[token]==self.exit:break
                self.instr[token]()
            self.steps+=1
            self.pntr+=1 if token>=len(self.tokens) else len(self.tokens[token])
            if showInternal and token<len(self.tokens):
                for i in self.vars:print(i+" = "+str(eval("self."+i)))
                print(f"\nInstruction #{str(self.steps)}:\nInstruction pointer: Position {self.pntr}\nExecuted instruction: {self.tokens[token]}\nCurrent output: {self.result}\n\n")
        print("\n\n\nOutput: "+self.result)
    def codeInput(self):self.run(input(f"\nInput {self.lang} code: "))

# Brainf**k
class Brainfk(EsoLang):
    def dpntrRight(self):
        self.dpntr+=1
        if self.dpntr>len(self.memory)-1:self.memory+=[0]
    def dpntrLeft(self):
        if self.dpntr<=0:self.memory.insert(0, 0)
        else:self.dpntr-=1
    def dpntrInc(self):self.memory[self.dpntr]+=1
    def dpntrDec(self):self.memory[self.dpntr]-=1
    def ouput(self):self.result+=chr(self.memory[self.dpntr]) if self.textMode and 0<=self.memory[self.dpntr]<=255 else str(self.memory[self.dpntr])+"\n"
    def input(self):
        if self.textMode:
            try:self.memory[self.dpntr]=ord(input("\nInput a character: ")[0])
            except IndexError:self.memory[self.dpntr]=-1
        else:
            try:self.memory[self.dpntr]=int(input("\nInput an integer: "))
            except ValueError:raise ValueError("invalid input")
    def loopStart(self):
        end=self.code[self.pntr+1:].find("]")
        if end<0:raise SyntaxError("unmatched '['")
        if self.memory[self.dpntr]==0 or self.loopMode and self.memory[self.dpntr]<0:
            end+=self.pntr+1
            layer=self.code[self.pntr+1:end].count("[")
            while layer>0:
                check=self.code[end+1:].find("]")
                if check<0:raise SyntaxError("unmatched '['")
                layer+=self.code[end+1:end+check+1].count("[")-1
                end+=check+1
            self.pntr=end
    def loopEnd(self):
        start=self.code[:self.pntr].rfind("[")
        if start<0:raise SyntaxError("unmatched ']'")
        if self.memory[self.dpntr]>0 or self.loopMode and self.memory[self.dpntr]<0:
            layer=self.code[start:self.pntr-1].count("]")
            while layer>0:
                check=self.code[:start].rfind("[")
                if check<0:raise SyntaxError("unmatched ']'")
                layer+=self.code[check:start].count("]")-1
                start=check
            self.pntr=start
    def __init__(self, loopStrict=False):
        super().__init__("Brainf**k", [">", "<", "+", "-", ".", ",", "[", "]"], [self.dpntrRight, self.dpntrLeft, self.dpntrInc, self.dpntrDec, self.ouput, self.input, self.loopStart, self.loopEnd], ["dpntr", "memory"], ["0", "[0]"])
        self.loopMode=loopStrict
    def run(self, code, textMode=False, showMem=False, showInternal=False):
        self.textMode=textMode
        super().run(code, showInternal)
        print(f"\nMemory: {self.memory}\nData pointer: Index {self.dpntr}\nOperations: {self.steps}\n" if showMem else "\n")
    def codeInput(self, textMode=False, showMem=False, showInternal=False):self.run(input(f"\nInput {self.lang} code: "), textMode, showMem, showInternal)
brainfk=Brainfk()

# Addition program
#brainfk.run(",<,[->+<]>.")

# Multiplication program
#brainfk.run(",<,[->[->+>+<<]>[-<+>]<<]>>>.")

# Exponential program (a^b)
#brainfk.run("+<,<,[->[->[->>+>+<<<]>+>[-<<+>>]<<<]>[-]>>>[-<<<+>>>]<<[-<<+>>]<<<]>>.")

# Hello world program
brainfk.run("++++++++[->+++++++++<]>.<++++++[->+++++<]>-.+++++++..+++.<++++++[-<+++++++<+++++>>]<++.<++.>[->++<]>-.>.+++.------.--------.<<<+.", True, True)

# Base 2 pentation (2^^^3 = 2^^4 = 2^16 = 65536)
#brainfk.run("+<+<+<+++[->[->[->[->+<]>[-<++>]<<]>[-<+>]+<<]>[-<+>]+<<]>.", False, True)

# Duplicating number A, B times
brainfk.run(",>,[[>]+[<]>[<+[>]<+[<]>>-]<[->+<]>>-]<[-]>>[-.>]", False, True)

# Triangular numbers ((n^2+n)/2)
#brainfk.run(",[->+>+<<]>[->[->+>+<<]>[-<+>]<<]>[->>+<<]>>[--<+>]<.", False, True)

# Ackermann function (m, n)
brainfk.run("->,>,<+[->>>>-<<<<[>>]>>+[-<[-<+>]<+>>>]+>+[[-<<<<<->>>>>]<<<<<[+>>]>[-<+>]<++++>]<[->]>[<<---<<--[++>>]>[-<++>]<++++>]>[-<+<---<[>]++<->>[-]>+>]<[-<<<[>]>-[-<<-<[->+<]<[->+>>+<<<]->>>[-<<<+>>>]]]>>[-]>[-]<<<<[>]<[->>>]<<<<+]>.", False, True)

# Quine (only works when loops are non-restrictive)
brainfk.run("-->+++>+>+>+>+++++>++>++>->+++>++>+>>>>>>>>>>>>>>>>->++++>>>>->+++>+++>+++>+++>+++>+++>+>+>>>->->>++++>+>>>>->>++++>+>+>>->->++>++>++>++++>+>++>->++>++++>+>+>++>++>->->++>++>++++>+>+>>>>>->>->>++++>++>++>++++>>>>>->>>>>+++>->++++>->->->+++>>>+>+>+++>+>++++>>+++>->>>>>->>>++++>++>++>+>+++>->++++>>->->+++>+>+++>+>++++>>>+++>->++++>>->->++>++++>++>++++>>++[-[->>+[>]++[<]<]>>+[>]<--[++>++++>]+[<]<<++]>>>[>]++++>++++[--[+>+>++++<<[-->>--<<[->-<[--->>+<<[+>+++<[+>>++<<]]]]]]>+++[>+++++++++++++++<-]>--.<<<]", True)

brainfk.codeInput(False, True)