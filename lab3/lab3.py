# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY, NEG_INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
##
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    score = 0
    if not board.is_game_over():
#        print " Not over yet "
        score = basic_evaluate(board)
    else:
        if board.is_win() == board.get_current_player_id():
#            print " Current win "
            score = 1000
        elif board.is_win() == board.get_other_player_id():
#            print " Opponent win "
            score = -1000
    return score

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
                      is_terminal_fn=is_terminal):

    return alpha_beta_search_aux(board,
                                 depth,
                                 eval_fn,
                                 get_next_moves_fn,
                                 is_terminal_fn,
                                 NEG_INFINITY,
                                 INFINITY)

def  alpha_beta_search_aux(board, depth, eval_fn,
                           get_next_moves_fn,
                           is_terminal_fn,
                           alpha, beta):
    best_val = None

    for move, new_board in get_next_moves_fn(board):
        val = -1 * ab_minimax_find_board_value(new_board, depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, negate(beta), negate(alpha))

        ## We always want to maximize our own utility. The current player's utility is valued by the negate of
        ##  the opponent's utility in this zero sum game.
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

        # Pruning won't happen at the root.

        # Update the value of alpha
        if alpha < val :
            alpha = val

    #if verbose:
    print "ALPHA-BETA: Decided on column %s with rating %s" % (best_val[1], best_val[0])

    return best_val[1]

def ab_minimax_find_board_value(board, depth, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta):

    best_val = None

    if is_terminal_fn(depth, board):
        return eval_fn(board)

    for move, new_board in get_next_moves_fn(board):
        val = -1 * ab_minimax_find_board_value(new_board, depth - 1, eval_fn, get_next_moves_fn, is_terminal_fn, negate(beta), negate(alpha))
        if best_val == None or val > best_val:
            best_val = val

        # Update the value of alpha
        alpha = max(alpha, val)

        if alpha >= beta:
            return alpha

    return val

def negate(n):
    if n == INFINITY:
        return NEG_INFINITY
    elif n == NEG_INFINITY:
        return INFINITY
    else:
        return -n

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

## Another stronger evaluation function can be built using the concept of threats.
## Threat is a square that connects 4 when a tile is dropped there by the opponent.
## You can simply return the difference in the number of threats by each player, but we can do much better by actually filtering useless threats (like a threat just above an opponents threat, or all threats above a threat by both players) and even assigning bonus for some threats (like lowermost threat of a column or 2 consecutive threats by the same player).
## -- From a comment of the post on http://stackoverflow.com/questions/10985000/how-should-i-design-a-good-evaluation-function-for-connect-4



def better_evaluate(board):
    current_player_id = board.get_current_player_id()
    score = 0
    if board.is_game_over():
        score = -1000
    elif board.is_win() == current_player_id:
        score = 1000
    elif board.is_win():
        score = -1000
    else:
        score = basic_evaluate(board)
        t1 = find_threats(board, board.get_current_player_id())
        t2 = find_threats(board, board.get_other_player_id())

        n_t1, n_t2 = filter_threats(t1, t2)
        score += (len(n_t1) - len(n_t2))
    return score

def find_threats(board, player_id):
    """
    Find all threats on the board for the specified player.
    Threat is a square that connects 4 when a tile is dropped there by the opponent.
    Return a set of cells that are threats.
    """
    for chain in board.chain_cells(player_id):
        print " chain cells for %s: %s" % (player_id, chain)
        pass
    return set([])

def filter_threats(threat_set_1, threat_set_2):
    """
    threat_set_1, threat_set_2: the sets of threat cells to be filtered.
    The rules are:
    1. If a threat just above an opponents threat;
    2. all threats above a threat by both players.

    returns tuple (filtered_threat_set_1, filtered_threat_set_2)
    """
    return (set([]), set([]))

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(better_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if True:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])

def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""
