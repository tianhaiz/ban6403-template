# Reviewed extraction sample (M11)

`m11_reviewed_dev.csv` holds 60 complaints from the `valid` split of `data/course/cfpb_complaints.csv`. Draft field labels were written with AI assistance and reviewed by the instructor. They were made by reading each complaint against the M11 extraction schema, version 1.2 (`data/llm_outputs/prompts/m11_extraction_schema.md`). Use them to check a rule baseline and saved LLM extractions field by field.

## How the sample was chosen

- 10 complaints per product (6 products), drawn at random from valid-split complaints of 50 to 180 words. In each product, 5 complaints contain a dollar amount (`{$...}`) and 5 do not, so both filled and missing amounts are well represented.
- Complaints already used in the M07 reviewed sample were left out.
- Three drawn complaints were replaced by the next random draw because they used insulting or disparaging language.
- `lab_sample` marks 20 complaints (3 per product plus 2 more, drawn at random) used in the guided part of Lab 11. The draw was repeated with the next random seed until every remedy label used in the full sample appeared at least once.
- These complaints are shorter than typical (the full dataset has a median of 168 words) and half contain an amount, which is more than in the full data (40%). Results here may not hold for the whole dataset.

## Columns

| Column | Meaning |
|---|---|
| complaint_id | Links to `cfpb_complaints.csv` (read the narrative there) |
| product, issue | Copied from the course dataset (the consumer's own choices) |
| n_words | Narrative length in words |
| lab_sample | `True` for the 20 complaints used in the guided part |
| disputed_amount | Dollar amount the complaint is mainly about; empty when missing |
| amount_evidence | Words copied exactly from the narrative that contain the amount |
| requested_remedy | `refund`, `correct_report`, `stop_or_validate_debt`, `account_action`, `review_or_explain`, `other` or `not_stated` |
| remedy_evidence | The words of the request, copied exactly; empty when `not_stated` |
| time_reference | First date or length of time about the problem, copied exactly; empty when missing |
| contacted_company | `yes`, `no` or `not_stated` |
| contact_evidence | Words that show the contact, copied exactly; empty when `not_stated` |
| review_note | Why a hard case was labeled the way it was (empty for most rows) |

An empty cell is a missing value: `null` for `disputed_amount` and `time_reference`, and `""` for the evidence columns.

## Limits

- How the labels were checked: a second reading covered every complaint and a third reading covered the harder ones. Disagreements were settled by majority or by a written rule, and the rules were added to the schema as version 1.2.
- Label summary: `disputed_amount` filled for 26 of 60, `time_reference` for 40 of 60; `requested_remedy` not_stated 20, correct_report 14, refund 12, account_action 7, stop_or_validate_debt 4, review_or_explain 3; `contacted_company` yes 37, not_stated 23. `review_note` is filled for 39 rows.
- The schema's rules decide most hard cases, but another careful reader could still choose differently. `review_note` flags the cases where this is most likely.
- Prompt `m11_extract_v2` was written from schema version 1, before the version 1.1 and 1.2 rules. Some of its disagreements with these labels come from those later rules.
- Every evidence span was checked by code: it appears exactly in the narrative.
