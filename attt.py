from functools import reduce
import sys

class advanced_tic_tac_toe:
    def __init__(self):
        self.s0 = []
        self.last_move = (-1, -1)
        for i in range(9): self.s0.append(['-'] * 9)
        sys.stderr.write("Choose your side ('x' or 'o'): ")
        sys.stderr.flush() # Make sure all of the message output before stdin
        side = (sys.stdin.readline()).strip()
        while side not in ['x', 'X', 'o', 'O']:
            sys.stderr.write("Invalid input, enter again: ")
            sys.stderr.flush()
            side = (sys.stdin.readline()).strip()
        self.human = 'x' if side in ['x', 'X'] else 'o'
        self.pc = 'x' if self.human == 'o' else 'o'
        self.show_once = 0 # When people make invalid inputs, only show the board for once.

    def player(self, s):
        if reduce((lambda x, y: x + y), [x.count('x') for x in s])\
        == reduce((lambda x, y: x + y), [x.count('o') for x in s]):
            return 'x'
        else:
            return 'o'

    def board_not_full(self, s):
        return [i for i, x in enumerate(s) if x.count('-') > 0]

    def single_board_over(self, s):
        if any([all([(x != '-' and x == s[0]) for x in s[:3]]),
               all([(x != '-' and x == s[3]) for x in s[3:6]]),
               all([(x != '-' and x == s[6]) for x in s[6:]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[3], s[6]]]),
               all([(x != '-' and x == s[1]) for x in [s[1], s[4], s[7]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[5], s[8]]]),
               all([(x != '-' and x == s[0]) for x in [s[0], s[4], s[8]]]),
               all([(x != '-' and x == s[2]) for x in [s[2], s[4], s[6]]])]):
            return 1
        elif s.count('-') == 0:
            return 0
        else:
            return -1

    def terminal_test(self, s):
        if any([any([self.single_board_over(x) == 1 for x in s]),
                all([self.single_board_over(x) == 0 for x in s])]):
            return True
        else:
            return False
        
    def cutoff_test(self, s, depth):
        return depth == 0 or self.terminal_test(s)

    def result(self, s, a):  # a[0]th board, position a[1].
        board = [x[:] for x in s]
        board[a[0]][a[1]] = self.player(s)
        self.last_move = a
        return board

    def action(self, s): # the rules are implemented here
        if self.last_move[0] < 0: #initial state
            return [(x, y) for x in range(9) for y in range(9)]
        else:
            valid_board = self.board_not_full(s)
            if self.last_move[1] not in valid_board: #already full, free to play
                return [(x, y) for x in valid_board for y in [i for i, z in enumerate(s[x]) if z == '-']]
            else:
                return [(self.last_move[1], y) for y in [i for i, x in enumerate(s[self.last_move[1]]) if x == '-']]
    
    def alpha_beta_search(self, s, depth = 3):
        return self.max_value(s, -float('inf'), float('inf'), depth)
    
    def max_value(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation(s), self.last_move
        v = -float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.min_value(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v > v:
                v, move = tmp_v, a
            if v >= beta: return v, move
            alpha = max(alpha, v)
        return v, move
    
    def min_value(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation(s), self.last_move
        v = float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.max_value(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v < v:
                v, move = tmp_v, a
            if v <= alpha: return v, move
            beta = min(beta, v)
        return v, move

    def show(self, s):
        if self.show_once == 0:  # 0 means not shown even once.
            sys.stderr.write(('|').join([(' ').join(s[0][:3]), (' ').join(s[1][:3]), (' ').join(s[2][:3])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[0][3:6]), (' ').join(s[1][3:6]), (' ').join(s[2][3:6])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[0][6:]), (' ').join(s[1][6:]), (' ').join(s[2][6:])]) + '\n')
            sys.stderr.write('-------------------' + '\n')
            sys.stderr.write(('|').join([(' ').join(s[3][:3]), (' ').join(s[4][:3]), (' ').join(s[5][:3])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[3][3:6]), (' ').join(s[4][3:6]), (' ').join(s[5][3:6])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[3][6:]), (' ').join(s[4][6:]), (' ').join(s[5][6:])]) + '\n')
            sys.stderr.write('-------------------' + '\n')
            sys.stderr.write(('|').join([(' ').join(s[6][:3]), (' ').join(s[7][:3]), (' ').join(s[8][:3])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[6][3:6]), (' ').join(s[7][3:6]), (' ').join(s[8][3:6])]) + '\n')
            sys.stderr.write(('|').join([(' ').join(s[6][6:]), (' ').join(s[7][6:]), (' ').join(s[8][6:])]) + '\n')
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
                    xy = (sys.stdin.readline()).strip()
                    x, y = xy[0], xy[-1]
                    a = (int(x) - 1, int(y) - 1)
                    if self.last_move[0] < 0: self.last_move = (0, a[0])
                    
                    #Little trick here. The '^' symbol is xor in python. Just judging if the input is valid or not.
                    while ((a[0] in self.board_not_full(s))^(a[0] == self.last_move[1])) or s[a[0]][a[1]] != '-':
                        sys.stderr.write("Invalid input, enter again: ")
                        sys.stderr.flush()
                        xy = (sys.stdin.readline()).strip()
                        x, y = xy[0], xy[-1]
                        a = (int(x) - 1, int(y) - 1)
                except Exception as e:
                    sys.stderr.write("Invalid input, enter again: ")
                    sys.stderr.flush()
                    continue
            else:
                val, a = self.alpha_beta_search(s, depth = 5)
                sys.stderr.write("Computer's move: ")
                sys.stderr.flush()
                sys.stdout.write(str(a[0] + 1) + ' ' + str(a[1] + 1) + '\n')
                sys.stdout.flush()
            s = self.result(s, a)
            self.show_once = 0

        self.show(s)

        if len(self.board_not_full(s)) == 0:
            sys.stderr.write("Tie!\n")
        else:
            if self.player(s) == self.pc:
                sys.stderr.write("You win!\n")
            else:
                sys.stderr.write("You lose!\n")
        
        sys.stderr.flush()

    def check_siege(self, s):
        cnt = 0
        for tmp in [s[:3], s[3:6], s[6:], [s[0], s[3], s[6]], 
                    [s[1], s[4], s[7]], [s[2], s[5], s[8]],
                    [s[0], s[4], s[8]], [s[2], s[4], s[6]]]:
            if tmp.count(self.human) == 2 and tmp.count(self.pc) == 1:
                cnt += 1
            elif tmp.count(self.human) == 1 and tmp.count(self.pc) == 2:
                cnt -= 1
        return cnt
    
    def evaluation(self, s): #making the pc win is always the goal
        points = 0
        for i in range(9):
            #for fixed points.
            if s[i][i] == self.pc: points += 1
            elif s[i][i] == self.human: points -= 1
            #for center points.
            if s[i][4] == self.pc: points += 1
            elif s[i][4] == self.human: points -= 1
            #for amount advantage.
            points += (s[i].count(self.pc) - s[i].count(self.human) - 1) * 3
            
            #winning bonus
            if self.single_board_over(s[i]) == 1:
                if self.player(s) == self.human:
                    points += 30
                else:
                    points -= 30
            
            #this is because if one sub-board is full, you can randomly play
            if self.last_move[1] == i and s[i].count('-') == 0:
                if self.player(s) == self.human:
                    points -= 10
                else:
                    points += 10
            
            #siege bonus
            points += self.check_siege(s[i]) * 3
            
        return points
    
g = advanced_tic_tac_toe()
g.play()
while 1:
    g.__init__()
    g.play()
