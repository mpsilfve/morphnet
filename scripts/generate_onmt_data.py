from sys import argv
from collections import defaultdict as dd
from random import shuffle

if __name__=='__main__':
    lanlist=argv[2:]
    targetdir=argv[1]

    for lan in lanlist:
        analyses = dd(set)
        for line in open('data/%s.ud' % lan):
            line = line.strip('\n')
            lang, wf, lemma, pos, msd = line.split('\t')
            lemma = ' '.join(lemma)
            wf = ' '.join(wf)
            msd = msd.split('|')
            a = '%s %s' % (lemma,
                           ' '.join(['+%s' % x for x in [pos] + msd]))
            analyses[wf].add(a)

        src_train = open('%s/%s-src-train.txt' % (targetdir,lan),'w')
        tgt_train = open('%s/%s-tgt-train.txt' % (targetdir,lan),'w')
        
        src_val = open('%s/%s-src-val.txt' % (targetdir,lan),'w')
        tgt_val = open('%s/%s-tgt-val.txt' % (targetdir,lan),'w')
        
        src_val_all = open('%s/%s-src-val.all.txt' % (targetdir,lan),'w')
        tgt_val_all = open('%s/%s-tgt-val.all.txt' % (targetdir,lan),'w')
        
        src_test = open('%s/%s-src-test.txt' % (targetdir,lan),'w')
        tgt_test = open('%s/%s-tgt-test.all.txt' % (targetdir,lan),'w')
        
        analyses = list(analyses.items())
        shuffle(analyses)
        
        for i,wf_analysis in enumerate(analyses):
            wf, analysis = wf_analysis
            if i % 10 < 8:
                for a in analysis:
                    print(wf,file=src_train)
                    print(a,file=tgt_train)
            elif i % 10 == 8:
                for a in analysis:
                    print(wf,file=src_val)
                    print(a,file=tgt_val)
                    print(wf,file=src_val_all)
                    print('\t'.join(analysis),file=tgt_val_all)
                else:
                    print(wf,file=src_test)
                    print('\t'.join(analysis),file=tgt_test)
