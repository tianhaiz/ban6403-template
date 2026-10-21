# Sentiment lexicon

`vader_lexicon_course.tsv` comes from the VADER sentiment lexicon (vaderSentiment 3.3.2, C.J. Hutto, MIT license; see `LICENSE_vader.txt`). Each row is a token and its average valence, from about -4 (very negative) to +4 (very positive), as rated by people.

Course changes: we kept only the token and mean valence columns, removed emoticons and other entries without letters, and removed profanity and insults. The full original lexicon and the VADER rules (negation, intensifiers, punctuation) are in the vaderSentiment package.
