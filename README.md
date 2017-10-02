# TicTacToe
Tic tac toe game. Try not lose!

Copyright: 2017, Shaojie Wang (swang115@ur.rochester.edu)

Environment: Fedora(Linux version 4.12.13-300.fc26.x86_64); python3 interpreter (version 3.6.2).

Guidance(steps):
0. Note that "ttt.py" is for normal 3*3 tic-tac-toe, and "attt.py" is for advanced tic-tac-toe.
1. Open terminal under the current path of tic-tac-toe programs.
2. Run the code with command line, "python3 ttt.py" for example.
3. Firstly, you should enter an 'x' or 'o' (quotation symbols not included) to indicate your side ('x' always for offensive side, and 'o' for defensive side).
4. After a board is shown on screen, you are asked to input your move. For simple 3*3 tic-tac-toe game, you only need to input one integer from 1 to 9, representing for the position as is shown below.
1 2 3
4 5 6
7 8 9
For advanced tic-tac-toe, you need to input two integers, both from 1 to 9. The first integer is for which board to play on, and the second one is for which position on that chosen board.
5. Each time you or the computer makes a move, a current board(state) will be shown on the screen. If the game is over, the result of the game will be shown. 
6. After that, a new game starts immediately (jump to step 3).
7. Ctrl+C to exit the program.

Cautions:
1. MUST use python3! NOT python!
2. The input should not contain any characters other than whitespace characters in the beginning and ending.
3. For advanced tic-tac-toe, you can input whatever you want (except '\n') between the two integers to separate them.
4. Make sure you type '\n' only when you finished your current input.

Updates:
- For the combat.py, you need to modify the evaluation functions manually. Automatic learning may come after.
