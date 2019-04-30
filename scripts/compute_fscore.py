from sys import argv

def readlines(fn):
    analyses = []
    for line in open(fn):
        line = line.strip('\n')
        if line != '':
            analyses.append(set(line.split('\t')))
    return analyses

def gettags(a):
    tags = set()
    for analysis in a:
        tags.add(' '.join([x for x in analysis.split(' ') if '+' in x]))
    return tags

def getlemmas(a):
    lemmas = set()
    for analysis in a:
        lemmas.add(' '.join([x for x in analysis.split(' ') if not '+' in x]))
    return lemmas

if __name__=='__main__':
    sys_analyses = readlines(argv[1])
    gold_analyses = readlines(argv[2])
    assert(len(sys_analyses) == len(gold_analyses))

    tp_a = 0.0
    fp_a = 0.0
    fn_a = 0.0

    tp_t = 0.0
    fp_t = 0.0
    fn_t = 0.0

    tp_l = 0.0
    fp_l = 0.0
    fn_l = 0.0

    for sysa, golda in zip(sys_analyses,gold_analyses):
        syst = gettags(sysa)
        goldt = gettags(golda)
        sysl = getlemmas(sysa)
        goldl = getlemmas(golda)

        tp_a += len(sysa.intersection(golda))
        fp_a += len(sysa.difference(golda))
        fn_a += len(golda.difference(sysa))

        tp_t += len(syst.intersection(goldt))
        fp_t += len(syst.difference(goldt))
        fn_t += len(goldt.difference(syst))

        tp_l += len(sysl.intersection(goldl))
        fp_l += len(sysl.difference(goldl))
        fn_l += len(goldl.difference(sysl))

    ra = tp_a / (tp_a + fn_a)
    pa = tp_a / (tp_a + fp_a)
    fa = 2 * pa * ra / (pa + ra)
    print("Analysis Recall: %.2f" % (100*ra))
    print("Analysis Precision: %.2f" % (100*pa))
    print("Analysis F-Score: %.2f" % (100*fa))

    print()
    rt = tp_t / (tp_t + fn_t)
    pt = tp_t / (tp_t + fp_t)
    ft = 2 * pt * rt / (pt + rt)
    print("Tag Recall: %.2f" % (100*rt))
    print("Tag Precision: %.2f" % (100*pt))
    print("Tag F-Score: %.2f" % (100*ft))

    print()
    rl = tp_l / (tp_l + fn_l)
    pl = tp_l / (tp_l + fp_l)
    fl = 2 * pl * rl / (pl + rl)
    print("Lemma Recall: %.2f" % (100*rl))
    print("Lemma Precision: %.2f" % (100*pl))
    print("Lemma F-Score: %.2f" % (100*fl))
