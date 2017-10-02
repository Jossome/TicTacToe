from functools import reduce

class Game:
    def __init__(self):
        self.s0 = []
        self.last_move = (-1, -1)
        for i in range(9): self.s0.append(['-'] * 9)
        side = input("evaluation1's side ('x' or 'o'): ")
        while side not in ['x', 'X', 'o', 'O']:
            side = input("invalid input, enter again: ")
        self.human = 'x' if side in ['x', 'X'] else 'o'
        self.pc = 'x' if self.human == 'o' else 'o'
        self.show_once = 0 # When people make invalid input, only show once.

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
        
    def get_current_depth(self, s):
        return reduce((lambda x, y: x + y), [x.count('-') for x in s])

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
    
    def show(self, s):
        if self.show_once == 0:  # 0 means not shown even once.
            print(s[0][:3], s[1][:3], s[2][:3])
            print(s[0][3:6], s[1][3:6], s[2][3:6])
            print(s[0][6:], s[1][6:], s[2][6:])
            print('------------------------' * 2)
            print(s[3][:3], s[4][:3], s[5][:3])
            print(s[3][3:6], s[4][3:6], s[5][3:6])
            print(s[3][6:], s[4][6:], s[5][6:])
            print('------------------------' * 2)
            print(s[6][:3], s[7][:3], s[8][:3])
            print(s[6][3:6], s[7][3:6], s[8][3:6])
            print(s[6][6:], s[7][6:], s[8][6:])
        self.show_once = 1  # already shown once, turn into 1.
    
#----------------------------------------------------------------------

    def alpha_beta_search1(self, s, depth = 3):
        return self.max_value1(s, -float('inf'), float('inf'), depth)
    
    def max_value1(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation1(s), self.last_move
        v = -float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.min_value1(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v > v:
                v, move = tmp_v, a
            if v >= beta: return v, move
            alpha = max(alpha, v)
        return v, move
    
    def min_value1(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation1(s), self.last_move
        v = float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.max_value1(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v < v:
                v, move = tmp_v, a
            if v <= alpha: return v, move
            beta = min(beta, v)
        return v, move

    def alpha_beta_search2(self, s, depth = 3):
        return self.max_value2(s, -float('inf'), float('inf'), depth)
    
    def max_value2(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation2(s), self.last_move
        v = -float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.min_value2(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v > v:
                v, move = tmp_v, a
            if v >= beta: return v, move
            alpha = max(alpha, v)
        return v, move
    
    def min_value2(self, s, alpha, beta, depth):
        if self.cutoff_test(s, depth):
            return self.evaluation2(s), self.last_move
        v = float('inf')
        move = self.action(s)[0]
        for a in self.action(s):
            tmp_v, _ = self.max_value2(self.result(s, a), alpha, beta, depth - 1)
            if tmp_v < v:
                v, move = tmp_v, a
            if v <= alpha: return v, move
            beta = min(beta, v)
        return v, move
    
    def check_siege1(self, s):
        cnt = 0
        for tmp in [s[:3], s[3:6], s[6:], [s[0], s[3], s[6]], 
                    [s[1], s[4], s[7]], [s[2], s[5], s[8]],
                    [s[0], s[4], s[8]], [s[2], s[4], s[6]]]:
            if tmp.count(self.human) == 1 and tmp.count(self.pc) == 2:
                cnt += 1
            elif tmp.count(self.human) == 2 and tmp.count(self.pc) == 1:
                cnt -= 1
        return cnt
    
    def check_siege2(self, s):
        cnt = 0
        for tmp in [s[:3], s[3:6], s[6:], [s[0], s[3], s[6]], 
                    [s[1], s[4], s[7]], [s[2], s[5], s[8]],
                    [s[0], s[4], s[8]], [s[2], s[4], s[6]]]:
            if tmp.count(self.human) == 2 and tmp.count(self.pc) == 1:
                cnt += 1
            elif tmp.count(self.human) == 1 and tmp.count(self.pc) == 2:
                cnt -= 1
        return cnt
    
    def evaluation1(self, s): #making the pc win is always the goal
        points = 0
        rest = reduce((lambda x, y: x + y), [x.count('-') for x in s])
        for i in range(9):
            #for fixed points. seems to be useless
            #if s[i][i] == self.pc: points -= 1
            #elif s[i][i] == self.human: points += 1
            #for center points.
            #if s[i][4] == self.pc: points -= 1
            #elif s[i][4] == self.human: points += 1
            #for amount advantage.
            
            points += (s[i].count(self.human) - s[i].count(self.pc) - 1) * (rest // 10)
            
            #winning bonus
            if self.single_board_over(s[i]) == 1:
                if self.player(s) == self.pc:
                    points += 30
                else:
                    points -= 30
            
            #this is because if one is full, you can suiyi put
            if self.last_move[1] == i and s[i].count('-') == 0:
                if self.player(s) == self.pc:
                    points -= 10
                else:
                    points += 10
            
            #siege
            points += self.check_siege1(s[i]) * 3
            
        return points    
    
    def evaluation2(self, s): #making the pc win is always the goal
        points = 0
        for i in range(9):
            #for fixed points. seems to be useless
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
            
            #this is because if one is full, you can suiyi put
            if self.last_move[1] == i and s[i].count('-') == 0:
                if self.player(s) == self.human:
                    points -= 10
                else:
                    points += 10
            
            #siege
            points += self.check_siege2(s[i]) * 3
            
        return points

    def combat(self):
        s = self.s0
        while not self.terminal_test(s):
            self.show(s)
            if self.player(s) == self.human:
                val, a = self.alpha_beta_search1(s, depth = 5)
                print("\neval1's turn:", a[0] + 1, a[1] + 1)
            else:
                val, a = self.alpha_beta_search2(s, depth = 5)
                print("\neval2's turn:", a[0] + 1, a[1] + 1)
            s = self.result(s, a)
            self.show_once = 0

        self.show(s)

        if len(self.board_not_full(s)) == 0:
            print("tie!")
        else:
            if self.player(s) == self.pc:
                print("evaluation1 win!")
            else:
                print("evaluation2 win!")

g = Game()
g.combat()