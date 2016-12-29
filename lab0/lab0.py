# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    import math
    return math.pow(x,3)

def factorial(x):
    if (not type(x) == int) or x < 0:
        raise ValueError

    if x == 0:
        return 1

    fac = x
    while (x > 1):
        x1 = x - 1
        fac = x1 * fac
        x -= 1
    return fac

def count_pattern(pattern, lst):
    count = 0
    pattern_length = len(pattern)
    while (pattern_length <= len(lst) ):
        if check_match(pattern, lst[:pattern_length]):
            count += 1
        lst = lst[1:]
    return count

def check_match(pattern, target_lst):
    for i in xrange(len(pattern)):
        if pattern[i] == target_lst[i]:
            pass
        else:
            return False
    return True

# Problem 2.2: Expression depth

class Node(object):
    def __init__(self, expr, depth):
        self.__depth = depth
        self.__expr = expr

    def depth(self):
        return self.__depth

    def expr(self):
        return self.__expr

def depth(expr):
    current_max_depth = 0
    import collections
    sub_exprs = collections.deque([])
    sub_exprs.appendleft(Node(expr, 0))
    while 1:
        try:
            node = sub_exprs.pop()

            ## update current_max_depth
            if node.depth() > current_max_depth:
                current_max_depth = node.depth()

            if isinstance(node.expr(), (list, tuple)):
                ## expand the expression if it still is a compound expression
                for expr in node.expr():
                    sub_exprs.appendleft(Node(expr, node.depth()+1))

        except IndexError:
            return current_max_depth


# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    raise NotImplementedError


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = ""

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = ""

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = ""

# How many hours did this lab take?
HOURS = ""
