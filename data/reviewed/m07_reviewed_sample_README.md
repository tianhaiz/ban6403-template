# Reviewed clothing review sample (M07)

`m07_reviewed_sample.csv` holds 120 reviews from the `valid` split of `data/course/clothing_reviews.csv`. Its labels are **draft labels written with AI assistance and reviewed by the instructor**, written against the codebook in `data/llm_outputs/prompts/m07_review_codebook.md`. The labels are a careful reference, not ground truth. Use them to check how well a lexicon score, an embedding classifier and saved LLM labels match that reading.

## How the sample was chosen

- 15 groups: five departments (Tops, Dresses, Bottoms, Intimate, Jackets) times three rating bands (1–2, 3 and 4–5 stars). Each group has 8 reviews, drawn at random (seed 6407). Trend and reviews without a department were left out.
- Low ratings are over-represented on purpose, so every group has the same denominator. In the full data, about 1 review in 10 has 1–2 stars; here, 1 in 3. A share from this sample is not a share of all reviews.
- The 120 reviews are part of the 360 reviews in `data/llm_outputs/m07_review_aspects_gemini.jsonl`.

## How the labels were made

1. A draft was written from the review text and the codebook only, before the saved LLM labels were made.
2. A second reader labeled the same 120 texts blind, without the draft, the ratings or the LLM labels.
3. The draft, the second reading and the saved LLM labels were compared, label by label. Where all three agree, that is the label. Otherwise the majority of the three decides. Three labels had no majority and were decided by two written rulings.
4. The edge cases found in the second reading are listed at the end of the codebook.

The draft and the second reading agreed on 115 of the 120 overall labels. Because the LLM labels were one of the three readings, comparisons between the LLM and this reference favor the LLM a little.

## Columns

| Column | Meaning |
|---|---|
| review_id | Links to `clothing_reviews.csv` (read `review_text`, `rating` and `department` there) |
| overall_sentiment | The writer's verdict on the item: `positive`, `negative` or `mixed` |
| n_aspects | Number of aspects with a label in this review (0 for review 116, which gives no aspect opinion; all its aspect cells are empty) |
| fit_size, fabric_quality, style_look, comfort, color, price_value | Sentiment toward that aspect: `positive`, `negative`, `mixed`, or empty when the review gives no opinion on it |
| fit_size_span, fabric_quality_span, … | Words copied exactly from `review_text` that show the aspect and its sentiment; empty when the aspect is empty |

Read the file with `keep_default_na=False`, so empty cells stay empty strings.

## Limits

- The labels are a majority of three readings against the codebook, not ground truth. Some opinions fit two aspects (for example "soft" fabric versus comfort). The tie-break rules decide, and another careful reader could still choose differently.
- About one review in five was cut off at about 500 characters in the source file. The labels cover the text that is there.
- Titles were not used.
