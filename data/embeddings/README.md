# Saved Embeddings

These files hold sentence embeddings that the instructor computed once, so every student gets the same numbers without downloading or running a model.

| File | Rows | What it is |
|---|---:|---|
| `clothing_minilm.npy` | 22,634 | One vector per review in `data/course/clothing_reviews.csv` (column `review_text`), same row order. Used in Lab 5. |
| `cfpb_minilm.npy` | 10,000 | One vector per complaint in `data/course/cfpb_complaints.csv` (column `narrative`), same row order |
| `cfpb_chunks_minilm.npy` | 16,073 | One vector per chunk in `data/processed/cfpb_chunks_150w.csv` (complaints split into pieces of about 150 words; Module 6), same row order |
| `feedback_minilm.npy` | 23 | One vector per example message with text (FB022 has no text) |
| `m05_sentences_minilm.npy` | 11 | One vector per example sentence in `data/raw/m05_demo_sentences.csv` |
| `m06_queries_minilm.npy` | 9 | One vector per query in `data/retrieval/m06_queries.csv` |
| `m12_passages_minilm.npy` | 70 | One vector per help-center passage in `data/rag/m12_kb_passages.csv` (column `search_text`), same row order |
| `m12_questions_minilm.npy` | 20 | One vector per support question in `data/rag/m12_questions.csv`, same row order |

Each `.npy` file has a matching `_ids.csv` (row number, ID, token count, whether the text was cut) and a `_manifest.json`.

## How the vectors were made

- Model: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` (Apache 2.0 license).
- Runtime: the model's official ONNX export, run with onnxruntime on a CPU.
- Input: the text column unchanged. No cleaning.
- Limit: 256 tokens. Longer texts are cut. No clothing review is cut (the longest has 162 tokens). 4,157 of the 10,000 complaints are cut, and 436 of the 16,073 complaint chunks. No example message, sentence, query, passage or question is cut.
- Pooling: the average of the token vectors, then scaled to length 1. Cosine similarity is therefore the dot product.
- Stored as float16 (384 numbers per row). Convert with `.astype("float32")` before use.
- The manifest stores a SHA-256 hash of the source file. Lab 5 shows how to check it.

Do not edit these files. If you add text of your own, embed it with the same model and revision, and never mix vectors from different models in one comparison.
