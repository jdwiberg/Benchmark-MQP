# Benchmark-MQP

## Access
This dataset can be found at https://huggingface.co/datasets/jdwiberg/benchmark-mqp-gs

## Dataset Overview
This dataset contains 100 manually annotated entity extraction files:
- 34 from Enron
- 33 from the unclassified WikiLeaks Hillary Clinton dataset
- The remainder (33) from the unclassified Epstein files

Some source text was edited to better suit entity extraction tasks, so the files do not necessarily reflect exact quotations. The annotations are not guaranteed to be perfect, but represent the best effort of human reviewers. This dataset is intended for benchmarking AI model performance against human annotations, not for training or fine-tuning. The JSON schema for each data point is shown in `example.json`.

## Judge Overview
The judge uses fuzzy string matching and tokenization to determine whether a found relationship triplet matches the answer key, and whether answer key triplets were found. It then computes precision (correct matches) and recall (coverage of answer key triplets).
