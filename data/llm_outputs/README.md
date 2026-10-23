# Saved LLM Outputs

These files hold answers that the instructor got from a large language model (LLM) once. You read the saved answers in the labs, so every student evaluates the same outputs. You never need an API key for required work.

| File | Rows | Input | Prompt version | Used in |
|---|---:|---|---|---|
| `m07_review_aspects_gemini.jsonl` | 360 | 360 clothing reviews (`review_text` only): the 120 in `data/reviewed/m07_reviewed_sample.csv` plus 240 more, 24 per department and rating band | `m07_review_aspects_v1` | Lab 7 Practice |
| `m07_feedback_aspects_gemini.jsonl` | 23 | The 23 example messages with text in `data/raw/customer_feedback_m01.csv` | `m07_feedback_aspects_v1` | Lab 7 guided part |
| `m08_route_valid_gemini.jsonl` | 300 | 300 `valid` complaints, drawn so each product keeps its share (narrative only) | `m08_route_v1` | Lab 8 Practice |
| `m08_route_test_gemini.jsonl` | 300 | 300 `test` complaints, drawn the same way (narrative only); sealed until Module 9 | `m08_route_v1` | Lab 9 final check |
| `m11_extract_v1_gemini.jsonl` | 60 | The 60 complaints in `data/reviewed/m11_reviewed_dev.csv` (narrative only) | `m11_extract_v1` | Lab 11 |
| `m11_extract_v2_gemini.jsonl` | 60 | The same 60 complaints | `m11_extract_v2` | Lab 11 |
| `m12_ungrounded_gemini.jsonl` | 20 | The 20 support questions in `data/rag/m12_questions.csv`, question only | `m12_ungrounded_v1` | Lab 12 |
| `m12_grounded_k1_gemini.jsonl` | 20 | The same questions with the top 1 passage | `m12_grounded_v1` | Lab 12 |
| `m12_grounded_k3_gemini.jsonl` | 20 | The same questions with the top 3 passages | `m12_grounded_v1` | Lab 12 |
| `m12_grounded_k8_gemini.jsonl` | 20 | The same questions with the top 8 passages | `m12_grounded_v1` | Lab 12 |
| `m13_heldout_extract_v2_gemini.jsonl` | 60 | The 60 held-out complaints in `data/heldout/m13_heldout_input.csv` | `m11_extract_v2` | Lab 13 (the frozen workflow) |
| `m13_heldout_extract_v2_gemini38flash.jsonl` | 60 | The same 60 complaints, model `gemini-3.8-flash` | `m11_extract_v2` | Lab 13 (model tiers) |
| `m13_heldout_extract_v2_gemini31pro.jsonl` | 60 | The same 60 complaints, model `gemini-3.1-pro-preview` | `m11_extract_v2` | Lab 13 (model tiers) |
| `m13_heldout_extract_v2_claude_opus55.jsonl` | 60 | The same 60 complaints, model `claude-opus-5-5` (Anthropic API) | `m11_extract_v2` | Lab 13 (model tiers) |
| `m13_injection_grounded_gemini.jsonl` | 3 | Three Module 12 questions with an injected forum post in the context (`prompts/m13_injection_input.csv`) | `m12_grounded_v1` | Lab 13 Practice |

The `m13_` files and `prompts/m13_injection_input.csv` are not in your repository from Week 1. They come in `m13_heldout_pack.zip` on the Module 13 page in Canvas. Unzip it and copy the files into the matching folders of your repository; the start of the Lab 13 notebook lists where each file goes.

The exact prompts, their JSON schemas and the aspect definitions are in `prompts/` (`m07_review_aspects_prompt.md`, `m07_review_aspects_schema.json`, `m07_feedback_prompt.md`, `m07_feedback_schema.json`, `m07_review_codebook.md`). The Module 8 routing prompt and its schema are `m08_route_prompt.md` and `m08_route_schema.json`. In each prompt, `{narrative}`, `{review_text}` or `{text}` marks where the input text was inserted; the Module 12 prompts use `{question}` and, in the grounded prompt, `{context}`.

For Module 11, `prompts/` also holds `m11_extraction_schema.md` (the field definitions, missing-value rules and validation rules), `m11_extract_schema.json` (the JSON schema both prompt versions had to follow), `m11_extract_v1_prompt.md` and `m11_extract_v2_prompt.md`. In the v2 prompt file, the example answers are written with double braces (`{{` and `}}`). The braces become single when the prompt is filled in, so the model saw ordinary JSON.

`m07_review_codebook.md` is the codebook for the Module 7 clothing review labels: six aspects, tie-break rules, sentiment per aspect and the overall sentiment. The prompt `m07_review_aspects_v1` contains the same definitions and rules.

## How the Module 7 outputs were made

- Model: `gemini-3.5-flash-lite`, as reported in each record's `model_version`. Temperature 0, with a JSON response schema, one call per input row.
- Example messages (`m07_feedback_aspects_gemini.jsonl`): Gemini API, October 14, 2026 (UTC). 23 of 23 answers parsed, with no errors. Median time per call about 0.85 seconds.
- Clothing reviews (`m07_review_aspects_gemini.jsonl`): Vertex AI (`api` = `vertex` in every record), October 15, 2026 (UTC; see `created`). 360 of 360 answers parsed, with no errors. Median time per call about 1.05 seconds. Input tokens in total: 332,274; output tokens: 47,327. Each record also has `thoughts_tokens`, which is empty (`null`): this model reported no thinking tokens. `m07_provenance_manifest.json` records the sample, the prompt and schema fingerprints and these counts.
- The prompt asks for each aspect at most once per review. In 21 cases the model gave the same aspect twice, and 13 of the 988 evidence spans are not exact copies of the text. Lab 7 checks both.

## Module 8 saved routing labels

- Model `gemini-3.5-flash-lite`, temperature 0, JSON response schema, one call per complaint. Settings and counts are also in `m08_route_manifest.json`.
- Module 8: 300 of 300 answers parsed for each split, with no errors (calls that hit a rate limit were retried, and only the successful call is kept). Median time per call about 0.8 seconds. Created October 14, 2026 (UTC).
- **Module 8 transport change.** Partway through the Module 8 run, the calls were sent through Vertex AI instead of the Gemini API. The model (`gemini-3.5-flash-lite`), prompt, schema and temperature did not change. Records sent through Vertex AI have `"api": "vertex"` (186 valid and 240 test records). Records without an `api` field were sent through the Gemini API (114 valid and 60 test records).
- The 300 valid and 300 test complaints were drawn by product and also by the Module 9 urgent flag, so each group keeps its share.

## Module 11 saved extractions

- Two prompt versions on the same 60 complaints, with the same model and the same JSON schema. Both follow `m11_extraction_schema.md` (version 1.2), the schema of the reviewed labels. Version 1 gives only the field names and label lists. Version 2 adds the full task specification from the schema, a rule to copy evidence exactly, and three example answers.
- **The three example answers in the v2 prompt were written by hand for the prompt.** They are made-up complaints, not model outputs, and they are not in the saved output files.
- Model: `gemini-3.5-flash-lite` (as reported in every record's `model_version`) through Vertex AI (`api` = `vertex` in every record), temperature 0, one call per complaint.
- Date: October 22, 2026 (UTC; see `created`).
- Results: 60 of 60 answers parsed for each version, with no errors. Median time per call about 1.07 seconds (v1) and 1.03 seconds (v2). Input tokens in total: 36,878 (v1) and 151,658 (v2), because the v2 prompt is about four times longer. Output tokens: 7,722 (v1) and 6,148 (v2).
- Parsed as JSON does not mean correct. Lab 11 checks every answer against the schema's validation rules and against the reviewed labels.
- `m11_provenance_manifest.json` is the provenance record for the Module 11 files. For each file it gives the kind of output (real model output, examples written by hand, reviewed labels or rule output). For the saved outputs it also gives the prompt version, model version, dates, row counts and token counts. Lab 11 asks you to build a smaller record of your own.

## Module 12 support answers

- One made-up help center (`data/rag/`), 20 made-up support questions, and four conditions. **Ungrounded**: the question only. **Grounded**: the question plus a context pack of the top 1, 3 or 8 passages from dense search. The grounded prompt says to use only the passages and to cite source IDs for every claim. It says to answer "not enough information" when the passages do not answer.
- The exact prompts are `prompts/m12_ungrounded_v1_prompt.md` and `prompts/m12_grounded_v1_prompt.md`, with the JSON schemas `m12_ungrounded_schema.json` and `m12_grounded_schema.json`. The filled inputs are `prompts/m12_input_ungrounded.csv` and `prompts/m12_input_grounded_k1.csv`, `_k3.csv` and `_k8.csv`. The `run_id` in these files (for example `Q12_k3`) is the `id` in the saved answer file.
- Model: `gemini-3.5-flash-lite` through Vertex AI (`api` = `vertex` in every record), temperature 0, one call per question and condition.
- Date: October 14, 2026 (UTC; see `created`).
- Results: 80 of 80 answers parsed, with no errors. Median time per call about 1.0 to 1.2 seconds. Input tokens in total: 6,173 (ungrounded), 10,359 (k = 1), 13,813 (k = 3) and 22,496 (k = 8).
- `m12_provenance_manifest.json` is the provenance record for the Module 12 files: the help center (written for this course), the embeddings, the context packs, the prompts, the four saved answer files and the drafted claim verdicts.

## Module 13 saved held-out and injection answers

- **Held-out extraction.** The frozen Module 11 prompt `m11_extract_v2`, with the same JSON schema, on 60 held-out complaints that were not used in Module 11 (`data/heldout/`). The prompt and the held-out labels follow the same schema (`m11_extraction_schema.md`, version 1.2). The same prompt was sent to three Gemini models through Vertex AI, at temperature 0:
  - `gemini-3.5-flash-lite` (the Module 11 workflow);
  - `gemini-3.8-flash`, a larger model;
  - `gemini-3.1-pro-preview`, a large model that Google labels **preview** (it may change or be withdrawn).
- **One model from another provider.** `claude-opus-5-5` (`m13_heldout_extract_v2_claude_opus55.jsonl`) received the same prompt through the Anthropic API, with the same JSON schema as structured output. This model does not accept a temperature setting, so it ran at its default (`temperature` is `null` in its records).
- Dates: October 22–23, 2026 (UTC; see `created`). 60 of 60 answers parsed for every model, with no errors.
- **Thinking tokens.** The two larger Gemini models think before they answer; all their records have a `thoughts_tokens` count. The `gemini-3.5-flash-lite` and `claude-opus-5-5` records report none (`null`). A missing value is not zero.
- **Token counts depend on the provider.** The three Gemini models report the same input count for the same filled prompt. The Claude records count about 1,000 more input tokens per complaint, because each provider splits text into tokens in its own way. Compare token counts within one provider.
- **Time.** `latency_ms` is the time the instructor's computer waited for each answer. It includes thinking time and any waiting at the service, and it depends on the day and the load. Median about 1.1 seconds (`gemini-3.5-flash-lite`), 15.7 seconds (`gemini-3.8-flash`), 16.0 seconds (`gemini-3.1-pro-preview`) and 4.0 seconds (`claude-opus-5-5`).
- **Prices are not included.** Cost is tokens times price, and prices change. Look up a price on the provider's price page and record the date if you need one.
- **Injection test.** `m13_injection_grounded_gemini.jsonl` holds three answers from the Module 12 grounded prompt `m12_grounded_v1` (`gemini-3.5-flash-lite`, Vertex AI, temperature 0, October 14, 2026). For questions Q05, Q06 and Q07, a made-up forum post, `FORUM-01` (status `unverified`), replaced one passage in the k = 3 context pack. The post contains an instruction aimed at the assistant. It was written for this test; it is not a real post. The filled inputs are in `prompts/m13_injection_input.csv`.
- `m13_provenance_manifest.json` is the provenance record for the Module 13 files: the held-out labels, the five saved answer files, and the prompt and schema fingerprints.

## What each line holds

Each line is one JSON record. It holds `id` (complaint_id, review_id, feedback_id or run_id, as text), `prompt_version`, `model`, `model_version`, `temperature` and `created`. It also holds `latency_ms`, `input_tokens` and `output_tokens`. Records sent through Vertex AI also hold `api` (`vertex`); records without it were sent through the Gemini API. Newer records also hold `thoughts_tokens`, the number of thinking tokens (`null` when the model reports none). Records sent through the Anthropic API have `api` = `anthropic`. Finally, `raw_text` is the model's answer as text, `parsed` is the answer as JSON, and `error` is empty when the call worked.

Read a file in Python with:

```python
records = [json.loads(line) for line in path.read_text().splitlines()]
```

## Things to know

- **Saved, not live.** These are saved answers from one run. If you send the same prompt again, even at temperature 0 or with the same model name, some answers may differ, because providers update models and serving systems.
- **A draft, not the truth.** The answers can be wrong. Each lab compares them with a reference set:
  - Labs 7 and 11: the reviewed samples in `data/reviewed`, and a check that every evidence span appears exactly in the text;
  - Lab 8: the CFPB product labels in `data/course/cfpb_complaints.csv`;
  - Lab 12: the drafted claim verdicts in `data/rag/m12_claim_audit_draft.csv`;
  - Lab 13: the held-out labels in `data/heldout/`.
- Only public course data, the made-up Module 12 help center and the made-up `FORUM-01` post were sent to the models. Do not edit these files; save your own outputs in `outputs/`.
