# RAG Files (Module 12)

These files support Lab 12. For this course we wrote a small help center for a bank called Fernhollow Financial, with its fees, deadlines and policies. We also wrote the 20 support questions used in the lab. The folder also holds the retrieval results behind each context pack and the claim verdicts.

| File | Rows | What it is |
|---|---:|---|
| `m12_kb_articles.csv` | 35 | Help-center articles: article_id, title, topic, effective_date, last_reviewed, status, n_passages |
| `m12_kb_passages.csv` | 70 | Each article split into short passages (23–60 words): passage_id, article_id, passage_no, title, topic, effective_date, last_reviewed, status, text, search_text, n_words |
| `m12_questions.csv` | 20 | Support questions Q01–Q20: question_id, question, question_type, expected_source_ids, related_source_ids, expected_behavior, reference_note, complaint_theme |
| `m12_retrieval_results.csv` | 400 | Top 10 passages per question for dense and TF-IDF search: question_id, method, rank, passage_id, score |
| `m12_context_packs_manifest.json` | – | How the context packs were built: retriever, k values, pack format and file hashes |
| `m12_claim_audit_draft.csv` | 162 | One row per claim in the four saved answer files: run_id, condition, question_id, claim_no, claim, cited_ids, verdict, citation_ok, evidence_ids, note, judged_by |

The passage and question vectors are in `data/embeddings/m12_passages_minilm.npy` and `m12_questions_minilm.npy`, each with an `_ids.csv` file and a manifest. They use the same model and revision as the Module 5 and Module 6 vectors. They were made once, together with the retrieval results and the context packs, on the same computer that produced the saved answers. A second build with the same model and scripts gave exactly the same ranks. The saved answers are in `data/llm_outputs/` (files `m12_*_gemini.jsonl`), and the exact prompts and inputs are in `data/llm_outputs/prompts/`.

## How the files were made

- **Passage IDs.** A passage ID is the article ID plus the passage number, for example `KB05-2`. IDs never change, so an answer can cite them.
- **search_text** is the article title, a period and the passage text. Both search methods use it, so a short passage keeps its topic.
- **Status.** `current` means the policy is in force. `archived` means it was replaced and is kept for history (KB11, replaced by KB10). One older Q&A article (KB03, effective 2021) was never updated; it disagrees with the current article KB01 on purpose.
- **Gaps on purpose.** Some topics have no article, for example the account of a customer who has died, auto loans, and recalling a wire. Questions about them cannot be answered from this help center.
- **Questions.** Some follow common themes in the course complaint data, without quoting any complaint; `complaint_theme` names the matching CFPB issue label.
  - `question_type` is answerable (13), partial (2), unanswerable (3), conflict (1: two sources disagree) or outdated (1: an archived source exists).
  - `expected_source_ids` lists the passages that answer the question; `related_source_ids` lists passages that are on topic but not needed, or that conflict. Both were drafted for this course before any search was run; `reference_note` gives the reason.
- **Context packs.** For each question, the top k passages from dense search (cosine of MiniLM vectors) are joined in rank order. Each block starts with `[passage_id] title | effective date | status`. Packs for k = 1, 3 and 8 are the inputs of the saved answers.
- **Claim verdicts** are draft verdicts written with AI assistance and reviewed by the instructor. Each claim was read against the help center, and a second reading checked every claim. The verdict rules:
  - `supported`: a current passage states the claim, or several current passages together state it. Hedged wording ("usually", "generally", "likely") is supported when the passage says the same.
  - `contradicted`: a current passage says something different (when two passages disagree, the newer effective date wins).
  - `unsupported`: no passage states the claim. This includes claims that say more than a passage does and inferences that no passage states. It also includes referrals that name specific steps or channels the help center does not give for that purpose.
  - `not_a_claim`: an apology, a bare referral to support ("contact customer support"), or a remark about the answer itself.
  - `citation_ok` (grounded answers only) is `yes` when the cited passage itself states the claim. Leave it blank for `not_a_claim`.
  - `judged_by` is `course draft`, or `student` for the 10 rows left blank for Lab 12 Exercise 2. Another careful reader may disagree on a few rows; `note` gives each reason.

Do not edit these files; save your own outputs in `outputs/`.
