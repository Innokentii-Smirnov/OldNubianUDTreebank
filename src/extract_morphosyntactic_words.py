import argparse
from os import path
from itertools import chain
from udapi.block.read.conllu import Conllu
import pandas as pd
from morphosyntactic_word import MorphosyntacticWord

parser = argparse.ArgumentParser(
  prog='extract_morphosyntactic_words.py',
  description='Extract words with annotations from a conllu-corpus'
)
parser.add_argument('infile')
parser.add_argument('outfile')
args = parser.parse_args()
assert path.exists(args.infile)
reader = Conllu(files=[args.infile])
document = reader.read_documents()[0]
morphosyntactic_words = set[MorphosyntacticWord]()
for node in chain.from_iterable(tree.descendants for tree in document.trees):
  morphosyntactic_word = MorphosyntacticWord(node.form,
                                             node.lemma,
                                             node.upos,
                                             str(node.feats),
                                             node.gloss,
                                             node.misc['MSeg'] or node.form)
  morphosyntactic_words.add(morphosyntactic_word)
df = pd.DataFrame(morphosyntactic_words)
df.sort_values(['form', 'lemma', 'upos', 'feats', 'gloss'], inplace=True)
df.to_csv(args.outfile, index=False, sep='\t',
          columns=['MSeg', 'lemma', 'feats', 'gloss', 'upos', 'form'])
