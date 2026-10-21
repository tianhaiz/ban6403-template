# Retrieval Files (Module 6)

These files support Lab 6. They let every student search with the same queries and score results against the same judgments, without running a model.

| File | Rows | What it is |
|---|---:|---|
| `m06_queries.csv` | 9 | The approved query set: TQ01–TQ04 for the 23 example messages, CQ01–CQ05 for the training complaints. Columns: query_id, query_set, query, information_need, filter_product, lab_use |
| `m06_relevance_judgments.csv` | 213 | Relevance judgments. Columns: query_id, doc_id, relevant, judged_by, note. relevant is 1, 0 or empty (for you to judge) |
| `m06_rerank_scores.csv` | 349 | Cross-encoder scores for query–text pairs: query_id, query, doc_id (feedback ID or chunk ID), text, query_set, complaint_id, chunk_no, lexical_rank, dense_rank, rerank_score, model, model_revision |

The query vectors are in `data/embeddings/m06_queries_minilm.npy`, with an `_ids.csv` file and a manifest. They were made with the same model and revision as the other vectors in that folder.

## How the files were made

- **Queries** were written before any search was run. Each query has a one-sentence information need.
- **Judgments** are draft judgments written with AI assistance and reviewed by the instructor. Each was made by reading the full message or complaint against the information need and this written rule:
  - A result is relevant when its main point matches the need.
  - Sharing a topic or a word is not enough.
  - Judge the content of the message or complaint against the information need. The product filter of a query is a search setting, not part of the need, so a complaint from another product can be relevant.
  - A solved problem does not count only when the need asks for an open problem (TQ03 "not yet fixed", TQ04 "has not reached them yet"). A need that asks whether the customer reports something (TQ01, TQ02) is met by a report of a past, solved case.
  - When the text does not say enough, the result is judged not relevant.
  - In the `judged_by` column, `course draft` marks these judgments and `student` marks the pairs left for you.
  - A second reading checked every judgment, and a third reading checked the harder ones. Disagreements were settled by majority or by the rules above.
- **What was judged:**
  - Queries on the example messages (TQ01–TQ04): every message.
  - Complaint queries: every complaint in the top 10 lexical, dense, filtered, whole-complaint, hybrid and reranked lists used in the lab.
  - Six complaint pairs are left empty for students.
- **Reranker:** `cross-encoder/ms-marco-MiniLM-L6-v2` (revision 233902d), official ONNX export, run on a CPU (about 11.6 ms per pair).
  - For complaint queries, the candidate pool is the top 20 complaints by lexical search plus the top 20 by dense search, searching the training chunks.
  - Every chunk of every pooled complaint was scored.
  - For the TQ queries, all 23 messages were scored.
  - Scores are raw model outputs: higher means more relevant. They are not probabilities.

Judgments are human decisions. Another careful reader may disagree on a few borderline cases; the `note` column gives each reason. Do not edit these files; enter your own judgments in the notebook.
