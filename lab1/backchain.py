from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    """
    1. Add the hypothesis to an OR tree.
    2. Read from the rules, match the consequent of each rule against the hypothesis:
    - If no match, then pass to next rule;
    - If there is a match, then:
        - instantiate the antescedent
        - add the instantiated antescendent, which is a new hypothesis, to the OR tree.
        - back chaining recursively.
    """
    raise NotImplementedError

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
