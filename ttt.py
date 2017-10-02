import sys

class tic_tac_toe:
    def __init__(self):
        self.s0 = ['-'] * 9
        sys.stderr.write("Choose your side ('x' or 'o'): ")
        sys.stderr.flush()
        side = (sys.stdin.readline()).strip()
        while side not in ['x', 'X', 'o', 'O']:
            sys.stderr.write("Invalid input, enter again: ")
            sys.stderr.flush()
            side = (sys.stdin.readline()).strip()
        self.human = 'x' if side in ['x', 'X'] else 'o'
        self.pc = 'x' if self.human == 'o' else 'o'
        self.show_once = 0 # When people make invalid input, only show the board for once.

    def player(self, s):
        return 'x' if s.count('x') == s.count('o') else 'o' 
        
    def action(self, s):
        return [i for i, x in enumerate(s) if x == '-']
        
    def result(self, s, a):
        board = s[:]
        board[a] = self.player(s)
        return board
        
    def terminal_test(self, s):
        if any([s.count('-') == 0,
               all([(x != '-' and x == s[0]) for x in s[:3]]),
               all([(x != '-' and x == s[3]) for x in s[3:6]]),
               all([(x != '-' and x == s[6]) for x in s[6:]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[3], s[6]]]),
               all([(x != '-' and x == s[1]) for x in [s[1], s[4], s[7]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[5], s[8]]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[4], s[8]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[4], s[6]]])]):
            return True
        else:
            return False
            
    def utility(self, s, p):  # calculate only when it is terminal state
        if any([all([(x != '-' and x == s[0]) for x in s[:3]]),
               all([(x != '-' and x == s[3]) for x in s[3:6]]),
               all([(x != '-' and x == s[6]) for x in s[6:]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[3], s[6]]]),
               all([(x != '-' and x == s[1]) for x in [s[1], s[4], s[7]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[5], s[8]]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[4], s[8]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[4], s[6]]])]):
            if p == self.human:  #human's turn then pc wins
                return 9 - s.count('-')
            elif p == self.pc:   #vice versa
                return -s.count('-')
        else:
            return 0
            
    def minimax(self, s):
        if self.terminal_test(s):
            return self.utility(s, self.player(s)), 0
        else:
            if self.player(s) == self.pc: #max
                res, index = -2, 0
                for a in self.action(s):
                    tmp, _ = self.minimax(self.result(s, a))
                    if tmp > res: res, index = tmp, a
                return res, index
            elif self.player(s) == self.human: #min
                res, index = 2, 0
                for a in self.action(s):
                    tmp, _ = self.minimax(self.result(s, a))
                    if tmp < res: res, index = tmp, a
                return res, index
    
    def show(self, s):
        if self.show_once == 0:  # 0 means not shown even once.
            sys.stderr.write((' ').join(s[:3]) + '\n')
            sys.stderr.write((' ').join(s[3:6]) + '\n')
            sys.stderr.write((' ').join(s[6:]) + '\n')
            sys.stderr.flush()
        self.show_once = 1  # already shown once, turn into 1.
    
    def play(self):
        s = self.s0
        while not self.terminal_test(s):
            self.show(s)
            if self.player(s) == self.human:
                try:
                    sys.stderr.write("Input your move: ")
                    sys.stderr.flush()
                    step = (sys.stdin.readline()).strip()
                    b = int(step) - 1
                    while s[b] != '-':
                        sys.stderr.write("Invalid input, enter again: ")
                        sys.stderr.flush()
                        step = (sys.stdin.readline()).strip()
                        b = int(step) - 1
                except Exception as e:
                    sys.stderr.write("Invalid input, enter again: ")
                    sys.stderr.flush()
                    continue
            else:
                val, b = self.minimax(s)
                sys.stderr.write("Computer's move: ")
                sys.stderr.flush()
                sys.stdout.write(str(b + 1) + '\n')
                sys.stdout.flush()
            
            s = self.result(s, b)
            self.show_once = 0

        self.show(s)
        
        if val > 0: #the minimax for computer is positive, meaning pc win and human lose
            sys.stderr.write("You lose!\n")
        elif val < 0: #vice versa
            sys.stderr.write("You win!\n")
        else: #if minimax value equals zero, then it is a game draw.
            sys.stderr.write("Tie!\n")
            
        sys.stderr.flush()

g = tic_tac_toe()
g.play()
while 1:
    g.__init__()
    g.play()
