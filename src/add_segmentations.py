import argparse
from os import path
from itertools import chain
from udapi.block.read.conllu import Conllu
import pandas as pd
from morphosyntactic_word import MorphosyntacticWord
from more_itertools import one

parser = argparse.ArgumentParser(
  prog='add_segmentations.py',
  description='Add segmentation from a lexicon to a conllu-corpus'
)
parser.add_argument('corpus')
parser.add_argument('lexicon')
args = parser.parse_args()
assert path.exists(args.corpus)
assert path.exists(args.lexicon)
df = pd.read_csv(args.lexicon, sep='\t', keep_default_na=False)
grouped = df.groupby(['form', 'lemma', 'upos', 'feats', 'gloss']).agg({'MSeg': lambda words: one(words)})
reader = Conllu(files=[args.corpus])
document = reader.read_documents()[0]
for node in chain.from_iterable(tree.descendants for tree in document.trees):
  morphosyntactic_word = grouped.loc[node.form, node.lemma, node.upos, str(node.feats), node.gloss if node.gloss != '_' else '']
  node.misc['MSeg'] = morphosyntactic_word.MSeg
document.store_conllu(args.corpus)
