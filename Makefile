ONMTPREPROCESS=~/OpenNMT-py/preprocess.py

LANGS=ast bak cat crh est fin fra ita kaz kir kpv mdf mhr mrj myv por sme spa tat tur udm
ROMLANGS=ast fra por ita cat spa
TURLANGS=crh bak kaz kir tat tur
GERLANGS=

all: opennmtdata models results eval

clean:
	rm -f opennmtdata/*pt opennmtdata/*txt models/*pt results/*txt

opennmtdata: $(LANGS:%=opennmtdata/%-src-train.txt) $(LANGS:%=opennmtdata/%.train.1.pt)

models: $(LANGS:%=models/%-model_step_10000.pt)

results: $(LANGS:%=results/%-src-test.txt.sys)

eval: $(LANGS:%=evaluation/%-src-test.txt.sys.eval)

opennmtdata/%-src-train.txt: data/%.ud
	python3 scripts/generate_onmt_data.py opennmtdata $*

%.train.1.pt:%-src-train.txt
	python3 $(ONMTPREPROCESS) -train_src $< -train_tgt $*-tgt-train.txt -valid_src $*-src-val.txt -valid_tgt $*-tgt-val.txt -save_data $*

scripts/onmt-train-%.sh:
	cat scripts/onmt-train.sh | sed "s/SOMELAN/$*/" > $@

scripts/onmt-test-%.sh:
	cat scripts/onmt-test.sh | sed "s/SOMELAN/$*/" > $@

models/%-model_step_10000.pt:opennmtdata/%.train.1.pt scripts/onmt-train-%.sh
	sbatch scripts/onmt-train-$*.sh

results/%-src-test.txt.nbest.out:scripts/onmt-test-%.sh models/%-model_step_10000.pt
	sbatch scripts/onmt-test-$*.sh

# These probability and firm threshold values need to be tuned using a
# development set. This target is for demonstration only.
results/%-src-test.txt.sys: results/%-src-test.txt.nbest.out
	cat $< | python3 scripts/get-analyses.py 0.7 2 opennmtdata/$*-src-test.txt > $@

evaluation/%-src-test.txt.sys.eval: results/%-src-test.txt.sys
	python3 scripts/compute_fscore.py results/$*-src-test.txt.sys opennmtdata/$*-tgt-test.all.txt > $@

sharedtaskdata/train/ast-track1:
	python3 scripts/generate_shared_task_data.py $(ROMLANGS)

sharedtaskdata/train/crh-track1:
	python3 scripts/generate_shared_task_data.py $(TURLANGS)

sharedtaskdata/train/GER-track1:
	python3 scripts/generate_shared_task_data.py $(GERLANGS)