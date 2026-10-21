# Saved Predictions from Module 8

These files hold the predictions of the Module 8 classifiers. They were made once with the same code and settings as the Lab 8 notebook. Module 9 reads them, so its results do not depend on your own Lab 8 run. Your Lab 8 run writes the same TF-IDF predictions to `outputs/m08`. Your own files keep every probability at full precision, while these copies round them to 4 decimals; both give the same Module 9 results.

| File | Rows | What it holds |
|---|---:|---|
| `m08_feedback_predictions.csv` | 10 | The 10 protected example messages: true follow-up label, baseline guess, TF-IDF prediction and probability of "yes" |
| `m08_route_predictions.csv` | 4,000 | The 2,000 `valid` and 2,000 `test` complaints: route predictions and probabilities from two classifiers, and the LLM label where one was cached |

## Columns of `m08_route_predictions.csv`

| Column | Meaning |
|---|---|
| `complaint_id`, `split` | Link to `data/course/cfpb_complaints.csv` |
| `route` | The product the consumer chose, as a short name (the label) |
| `tfidf_route`, `tfidf_p_<route>` | TF-IDF + logistic regression: predicted route and one probability per route (the six add up to 1) |
| `emb_route`, `emb_p_<route>` | Logistic regression on the `cfpb_minilm` embeddings: predicted route and probabilities |
| `llm_route` | Zero-shot LLM label (prompt `m08_route_v1`), empty if the complaint was not sent |
| `in_llm_subset` | True for the 300 `valid` and 300 `test` complaints that were sent to the LLM. Each set was drawn to keep the split's product shares and its share of Module 9 urgent complaints. |

Short route names: `checking`, `credit_card`, `credit_reporting`, `debt_collection`, `money_transfer`, `mortgage`.

## How they were made

- Both classifiers were fitted on the 6,000 `train` complaints only. TF-IDF settings: words and two-word phrases, `min_df=5`, stop words `xx` and `xxxx`. Logistic regression with `max_iter=1000` and default settings otherwise.
- The LLM labels come from `data/llm_outputs/m08_route_valid_gemini.jsonl` and `m08_route_test_gemini.jsonl`.
- Probabilities are rounded to 4 decimals.

## Things to know

- **The test rows are sealed.** Do not score them in Module 8. Module 9 opens them once, after its decision policy is fixed.
- **The `route` label is the consumer's choice.** It can be wrong, so some "errors" are label questions.
- Do not edit these files. Save your own outputs in `outputs/`.
