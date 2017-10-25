import sexpParser as sp

test1 = "x,y := (+ x y), x"
test2 = "a, b, c := (ite c b a), (vector-ref ar i), (&& (! (vector-ref ar i) b))"
alltests = [locals()[t] for t in sorted(locals()) if t.startswith("test")]


def parseexpr(s):
    return sp.sexp.parseString(s, parseAll=True).asList()


class ParallelAssignments(object):

    def __init__(self, passgn):
        lh_and_rh = passgn.split(':=')
        assert len(lh_and_rh) == 2
        self.raw_lhs = lh_and_rh[0].split(',')
        self.raw_rhs = map(parseexpr, lh_and_rh[1].split(','))
        assert len(self.raw_lhs) == len(self.raw_rhs)

    def __str__(self):
        return "%s := %s" % (", ".join(self.raw_lhs), ", ".join(map(str, self.raw_rhs)))


for t in alltests:
    print '-' * 50
    print t
    try:
        print ParallelAssignments(t)
    except sp.ParseFatalException, pfe:
        print "Error:", pfe.msg
        print pfe.markInputline('^')
    print


