# Data

| file | what it is |
|---|---|
| `lmeval_tasks.json` | the ARC-Easy and HellaSwag items used for the downstream evaluation |
| `corpus_gpt2bpe_48000000.npy.meta.json` | parameters of the tokenized training corpus |

## The corpus is not in this repository

`corpus_gpt2bpe_48000000.npy` is 92 MB and fully regenerable, so it is excluded
by `.gitignore`. It is the public FineWeb-EDU `sample-10BT` stream tokenized
with the public GPT-2 byte-pair encoder to 48 M tokens, vocabulary 50,257.
`code/TAI_fast.ipynb` rebuilds it on first run and writes it to this directory.

No proprietary or personal data were used anywhere in the study.
