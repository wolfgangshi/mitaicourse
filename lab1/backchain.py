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
    requirements = [hypothesis]
    for r in rules:
        binding = match_hypothesis_against_consequents(r.consequent(), hypothesis)
        if not (isinstance(binding, dict) or binding):
            continue
        else:
            new_hypotheses = populate(r.antecedent(), binding)

        ## Recursively back chaining on the new hypotheses.
        if isinstance(new_hypotheses, basestring):
            requirements.append( backchain_to_goal_tree(rules, new_hypotheses) )
        else:
            requirements.append( new_hypotheses.__class__(*[backchain_to_goal_tree(rules, h) for h in new_hypotheses]) )

    return simplify(OR(requirements))

def match_hypothesis_against_consequents(consequents, hypothesis):
    for c in consequents:
        binding = match(c, hypothesis)
        if (not isinstance(binding, dict)) and (not binding):
##            print "match_hypothesis_against_consequents: no match found with rules '%s' for hypothesis: '%s'" % (c, hypothesis)
            continue
        else:
            ## Once a binding is found, return.
            return binding
    return None


# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')

if __name__ == '__main__':
    RULES =  IF( AND( '(?x) is a bird',        # Z15
                      '(?x) is a good flyer' ),
                 THEN( '(?x) is an albatross' ))
    assert(backchain_to_goal_tree([RULES], "abc") == 'abc')
    assert(backchain_to_goal_tree([RULES], "a is an albatross") ==
           OR("a is an albatross", AND('a is a bird', 'a is a good flyer') )
    )
