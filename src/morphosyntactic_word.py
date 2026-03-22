from dataclasses import dataclass

@dataclass(frozen=True)
class MorphosyntacticWord:
  form: str
  lemma: str
  upos: str
  feats: str
  gloss: str
  MSeg: str
