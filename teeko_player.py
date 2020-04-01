"""/////////////////////////////////////////////////////////////////////////////
// Main File:        teeko_player.py
// This File:        teeko_player.py
// Other Files:
// Semester:         CS 540 Spring 2020
//
// Author:           Runze Li
// Email:            rli263@wisc.edu
// CS Login:         runze
//
/////////////////////////// OTHER SOURCES OF HELP ///////////////////////////"""
import random
import time


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def copy_state(self, b):
        a = [[' ' for j in range(5)] for i in range(5)]

        for i in range(len(b)):
            for j in range(len(b[i])):
                a[i][j] = b[i][j]
        return a

    """
    This method returns all legal successor states of current state
    is_drop checks if it is a drop phase
    label is the current color that should move
    """
    def succ(self, state, is_drop, label):
        successor = []

        # drop phase
        if is_drop is True:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ':
                        temp = self.copy_state(state)
                        temp[i][j] = label
                        successor.append(temp)
        # not drop phase
        else:
            pos_list = []
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == label:
                        pos_list.append((i, j))
            # add all possible moves to the successor list
            for i in pos_list:
                if i[1] - 1 >= 0 and state[i[0]][i[1] - 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0]][i[1] - 1] = label
                    successor.append(temp)
                if i[1] + 1 <= 4 and state[i[0]][i[1] + 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0]][i[1] + 1] = label
                    successor.append(temp)
                if i[0] - 1 >= 0 and state[i[0] - 1][i[1]] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] - 1][i[1]] = label
                    successor.append(temp)
                if i[0] + 1 <= 4 and state[i[0] + 1][i[1]] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] + 1][i[1]] = label
                    successor.append(temp)
                if i[0] + 1 <= 4 and i[1] + 1 <= 4 and state[i[0] + 1][i[1] + 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] + 1][i[1] + 1] = label
                    successor.append(temp)
                if i[0] + 1 <= 4 and i[1] - 1 >= 0 and state[i[0] + 1][i[1] - 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] + 1][i[1] - 1] = label
                    successor.append(temp)
                if i[0] - 1 >= 0 and i[1] - 1 >= 0 and state[i[0] - 1][i[1] - 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] - 1][i[1] - 1] = label
                    successor.append(temp)
                if i[0] - 1 >= 0 and i[1] + 1 <= 4 and state[i[0] - 1][i[1] + 1] == ' ':
                    temp = self.copy_state(state)
                    temp[i[0]][i[1]] = ' '
                    temp[i[0] - 1][i[1] + 1] = label
                    successor.append(temp)

        return successor


    """
    This method checks the number of markers in the winning location
    including vertical, horizontal, box and diagonal
    """
    def check_in_place(self, state, pos, label):

        """---check for vertical---"""
        i = pos[0]
        j = pos[1]
        num_vert = 0
        while i > 0:
            i = i - 1
            if state[i][j] == label:
                num_vert += 1
            elif state[i][j] != ' ':
                break
        i = pos[0]
        j = pos[1]
        while i < 4:
            i = i + 1
            if state[i][j] == label:
                num_vert += 1
            elif state[i][j] != ' ':
                break
        num_vert = num_vert * 0.25
        """---check for horizontal---"""
        i = pos[0]
        j = pos[1]
        num_hori = 0
        while j > 0:
            j = j - 1
            if state[i][j] == label:
                num_hori += 1
            elif state[i][j] != ' ':
                break
        i = pos[0]
        j = pos[1]
        while j < 4:
            j = j + 1
            if state[i][j] == label:
                num_hori += 1
            elif state[i][j] != ' ':
                break
        num_hori = num_hori * 0.25
        """---check for diagonal \ ---"""
        i = pos[0]
        j = pos[1]
        num_lud = 0  # \
        while j > 0 and i > 0:
            j = j - 1
            i = i - 1
            if state[i][j] == label:
                num_lud += 1
            elif state[i][j] != ' ':
                break
        i = pos[0]
        j = pos[1]
        while j < 4 and i < 4:
            j = j + 1
            i = i + 1
            if state[i][j] == label:
                num_lud += 1
            elif state[i][j] != ' ':
                break
        num_lud = num_lud * 0.25
        """---check for diagonal / ---"""
        i = pos[0]
        j = pos[1]
        num_rud = 0  # /
        while j < 4 and i > 0:
            j = j + 1
            i = i - 1
            if state[i][j] == label:
                num_rud += 1
            elif state[i][j] != ' ':
                break
        i = pos[0]
        j = pos[1]
        while j > 0 and i < 4:
            j = j - 1
            i = i + 1
            if state[i][j] == label:
                num_rud += 1
            elif state[i][j] != ' ':
                break
        num_rud = num_rud * 0.25
        """---check for box ---"""
        i = pos[0]
        j = pos[1]
        num_box = -1

        for m in [i-1, i, i + 1]:
            for n in [j - 1, j, j + 1]:
                if m >= 0 and m <= 4 and n >= 0 and n<= 4 and state[m][n] == label:
                    num_box += 1
                elif m >= 0 and m <= 4 and n >= 0 and n<= 4 and state[m][n] != ' ':
                    num_box = num_box - 1

        if num_box < 0:
            num_box = 0
        num_box = num_box * 0.25

        # return the maximum of all
        return max([num_box, num_hori, num_vert, num_lud, num_rud]) - 0.01


    def heuristic_game_value(self, state):

        # call game_value first, check if it is the end state
        checker = self.game_value(state)
        if checker == 1 or checker == -1:
            return checker

        pos_list = []
        pos_list_2 = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece:
                    pos_list.append((i, j))
                if state[i][j] == self.opp:
                    pos_list_2.append((i, j))

        if len(pos_list) == 0 and len(pos_list_2) == 0:
            return 0

        minplay = 0
        maxplay = 0

        """evaluate the maximum in placed markers 
        for both players, one positive and one negative"""
        if len(pos_list) != 0:
            score = []

            for i in range(len(pos_list)):
                score.append(self.check_in_place(state, pos_list[i], self.my_piece))

            maxplay = max(score)


        if len(pos_list_2) != 0:
            score_2 = []
            for i in range(len(pos_list_2)):
                score_2.append(self.check_in_place(state, pos_list_2[i], self.opp))

            minplay = -1 * max(score_2)

        """return the sum as heuristic 
        points of current state"""
        return maxplay + minplay


    """
    Max player's level
    """
    def Max_Value(self, state, depth, limit, is_drop):

        # check the end state
        curr_val = self.heuristic_game_value(state)
        if depth == limit or curr_val == 1 or curr_val == -1:
            return curr_val, state

        a = -2  # -2 is - infinity here
        curr = None
        # get successors
        successor_list = self.succ(state, is_drop, self.my_piece)

        depth += 1  # one more depth

        """ iterate through the successor list and call 
        Min player's level, return the one with max points"""
        for succ in successor_list:
            is_drop = self.drop_check(succ)
            val, temp = self.Min_Value(succ, depth, limit, is_drop)
            # return the max point and this state
            if a <= val:
                a = val
                curr = succ

        return a, curr

    """
    Min player's level
    """
    def Min_Value(self, state, depth, limit, is_drop):

        # check the end state
        curr_val = self.heuristic_game_value(state)
        if depth == limit or curr_val == 1 or curr_val == -1:
            return curr_val, state

        b = 2  # 2 is infinity here
        curr = None
        successor_list = self.succ(state, is_drop, self.opp)

        depth += 1

        """ iterate through the successor list and call 
        Min player's level, return the one with max points"""
        for succ in successor_list:
            is_drop = self.drop_check(succ)
            val, temp = self.Max_Value(succ, depth, limit, is_drop)
            # return the max point and this state
            if b >= val:
                b = val
                curr = succ

        return b, curr


    """
    This method returns if current state is in the drop phase
    """
    def drop_check(self, state):
        drop_phase = True

        counter = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    counter = counter + 1
        if counter == 8:
            drop_phase = False

        return drop_phase

    """
    Make move based on min max algo and current state
    """
    def make_move(self, state):

        # check for drop phase
        drop_phase = self.drop_check(state)

        move = []

        # set the level we zoom into
        if drop_phase is True:
            limit = 3
        else:
            limit = 3

        copy = self.copy_state(state)

        """Call the minmax algorithm to determine next state we choose"""
        val, curr = self.Max_Value(copy, 0, limit, drop_phase)

        dest = None
        src = None

        """Extract how to move from the next state we choose to reach"""
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == ' ' and curr[i][j] == self.my_piece:
                    dest = (i, j)
                if state[i][j] == self.my_piece and curr[i][j] == ' ':
                    src = (i, j)

        move.append(dest)

        # if it is not drop phase, add second option
        if src is not None:
            move.append(src)

        return move


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins

        pos_list = []
        pos_list_2 = []
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == self.my_piece:
                    pos_list.append((i, j))
                if state[i][j] == self.opp:
                    pos_list_2.append((i, j))
        pos_list.sort()
        pos_list_2.sort()

        try:
            if len(pos_list) == 4:
                if pos_list[0][0] + 1 == pos_list[1][0] and pos_list[0][1] + \
                        1 == pos_list[1][1] and pos_list[1][0] + 1 == pos_list[2][0] and pos_list[1][1] \
                        + 1 == pos_list[2][1] and pos_list[2][0] + 1 == pos_list[3][0] and pos_list[2][1] \
                        + 1 == pos_list[3][1]:
                    return 1
        except:
            pass

        try:
            if len(pos_list_2) == 4:
                if pos_list_2[0][0] + 1 == pos_list_2[1][0] and pos_list_2[0][1] + \
                        1 == pos_list_2[1][1] and pos_list_2[1][0] + 1 == pos_list_2[2][0] and pos_list_2[1][1] \
                        + 1 == pos_list_2[2][1] and pos_list_2[2][0] + 1 == pos_list_2[3][0] and pos_list_2[2][1] + 1 == \
                        pos_list_2[3][1]:
                    return -1
        except:
            pass

        # check / diagonal wins
        try:
            if len(pos_list) == 4:
                if pos_list[0][0] + 1 == pos_list[1][0] and pos_list[0][1] - \
                        1 == pos_list[1][1] and pos_list[1][0] + 1 == pos_list[2][0] and pos_list[1][1] \
                        - 1 == pos_list[2][1] and pos_list[2][0] + 1 == pos_list[3][0] and pos_list[2][1] \
                        - 1 == pos_list[3][1]:
                    return 1
        except:
            pass

        try:
            if len(pos_list_2) == 4:
                if pos_list_2[0][0] + 1 == pos_list_2[1][0] and pos_list_2[0][1] - \
                        1 == pos_list_2[1][1] and pos_list_2[1][0] + 1 == pos_list_2[2][0] and pos_list_2[1][1] \
                        - 1 == pos_list_2[2][1] and pos_list_2[2][0] + 1 == pos_list_2[3][0] and pos_list_2[2][1] - 1 == \
                        pos_list_2[3][1]:
                    return -1
        except:
            pass

        # check 2x2 box wins
        try:
            if len(pos_list) == 4:
                if pos_list[0][1] + 1 == pos_list[1][1] and pos_list[0][0] == pos_list[1][0] \
                        and pos_list[0][0] + 1 == pos_list[2][0] and pos_list[0][1] == pos_list[2][1] \
                        and pos_list[0][0] + 1 == pos_list[3][0] and pos_list[0][1] + 1 == pos_list[3][1]:
                    return 1
        except:
            pass

        try:
            if len(pos_list_2) == 4:
                if pos_list_2[0][1] + 1 == pos_list_2[1][1] and pos_list_2[0][0] == pos_list_2[1][0] \
                        and pos_list_2[0][0] + 1 == pos_list_2[2][0] and pos_list_2[0][1] == pos_list_2[2][1] \
                        and pos_list_2[0][0] + 1 == pos_list_2[3][0] and pos_list_2[0][1] + 1 == pos_list_2[3][1]:
                    return -1
        except:
            pass
        
        return 0 # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
        print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp+"'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                 (int(move_from[1]), ord(move_from[0])-ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
