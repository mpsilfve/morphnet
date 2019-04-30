from sys import argv, stderr
from random import shuffle, seed
from collections import defaultdict as dd

seed(0)

def readdata(lan):
    analyses = dd(lambda : [])

    for line in open("data/%s.ud" % lan):
        line = line.strip("\n")
        if line:
            lan, wf, lemma, pos, mor = line.split('\t')
            analyses[wf].append((lan, lemma, pos, mor))

    analyses = sorted(analyses.items())
    shuffle(analyses)
    return analyses

def getsplit(data):
    train = []
    dev = []
    test = []
    
    for i,a in enumerate(data):
        if i % 10 == 8:
            dev.append(a)
        elif i % 10 == 9:
            test.append(a)
        else:
            train.append(a)
    
    return train, dev, test

def writedata(data,fn,cover=0):
    ofile = open(fn,"w")
    for wf, analyses in data:
        lan = analyses[0][0]
        if cover:
            print("\t".join([lan,wf,"_","_","_"]), file=ofile)
        else:
            for lan, lemma, pos, mor in analyses:
                print("\t".join([lan,wf,lemma,pos,mor]), file=ofile)
    
if __name__=="__main__":
    if len(argv) < 3:
        print("USAGE: %s testlanguage trainlanguage1 trainlanguage2 ...", 
              stderr)
        exit(1)

    targetlan = argv[1]
    relatedlans = argv[2:]
    targetdata = readdata(targetlan)
    relateddata = [readdata(lan) for lan in relatedlans]

    targettraindata, targetdevdata, targettestdata = getsplit(targetdata) 

    track1traindata = targettraindata
    track2traindata = targettraindata + [a for d in relateddata for a in d]
    track3traindata = [a for d in relateddata for a in d]

    shuffle(track1traindata)
    shuffle(track2traindata)
    shuffle(track3traindata)

    writedata(track1traindata,"sharedtaskdata/train/%s-track1-uncovered" 
              % targetlan)
    writedata(track2traindata,"sharedtaskdata/train/%s-track2-uncovered" 
              % targetlan)
    writedata(track3traindata,"sharedtaskdata/train/%s-track3-uncovered" 
              % targetlan)

    writedata(targetdevdata,"sharedtaskdata/dev/%s-uncovered" % targetlan)
    writedata(targetdevdata,"sharedtaskdata/dev/%s-covered" % targetlan, 
              cover=1)

    writedata(targettestdata,"sharedtaskdata/test/%s-uncovered" % targetlan)
    writedata(targettestdata,"sharedtaskdata/test/%s-covered" % targetlan, 
              cover=1)
