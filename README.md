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

## Explanation of EE
Our goal with the dataset is to make a benchmarking tool for AI Entity Extraction (EE). To us, this means identifiying all instances of a reference to a **Target Entity**.

A target entity is either a person or an organization. In the "target_entity" slot of the key, we use the most formal reference to the target entity we could find. For example, if "Jeffrey Epstein" had references: "JE", "Jeff", "The big guy", "Jeffrey Epstein", "jeffrey E.", we used his full properly capitalized name. If instead the only reference to an entity was "her", we would use "her". This is somewhat of a judgement call.

Which each instance of a reference to an entity, we aimed to classify it into one of four categories:
- Direct Reference (DR), any direct reference using a name or pronoun (ex: Jeff, him, we, our, I'll, I'm, their, they etc)
- Sensitive Information (SI), information that isn't public knowledge and could be sensitive like personal email address, phone number, precise location, SSN etc
- Non-Personal Unique Information (NPUI), information that is unique to a certain entity but non necessarily private or sensitive like business email, professional headquarters, or descriptive physical information
- Personal Health Information (PHI), information related to the personal health of an entity like recent illness, surgery date or type, age, or general health status.

We aim to test a model's ability to identify ALL references to a target entity and correctly classify them. To do this, a model must output a key.json file of the same format as our datasets keys for each text file.