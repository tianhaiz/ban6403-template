# Course Dataset: Women's E-Commerce Clothing Reviews

`clothing_reviews.csv` holds 22,634 real customer reviews from an online women's clothing store. Each row is one review, written by a customer, with the star rating they gave and the store's product categories. Labs 4, 5 and 7 use it for Practice.

## Columns

| Column | Meaning |
|---|---|
| review_id | Row number of the review in the source file. Use it to link outputs back to the text. |
| clothing_id | ID of the item reviewed (1,177 different items) |
| age | Reviewer's age, as given in the source (18 to 99). We cannot check it. |
| title | Short title of the review. Empty for 2,965 reviews (13%). |
| review_text | The review in the customer's own words |
| rating | Stars the customer gave, from 1 (worst) to 5 (best) |
| recommended | 1 if the customer recommends the item, 0 if not |
| positive_feedback_count | How many other customers marked the review as helpful (0 to 122; 0 for 46% of reviews) |
| division | Store division: General, General Petite or Initmates (sic) |
| department | Store department (6 departments, see below) |
| class_name | Finer product class, such as Knits, Blouses, Jeans or Swim (20 classes) |
| split | `train` (13,581), `valid` (4,528) or `test` (4,525). Do not change it. |

| Department | Rows |
|---|---:|
| Tops | 10,046 |
| Dresses | 6,144 |
| Bottoms | 3,661 |
| Intimate | 1,650 |
| Jackets | 1,002 |
| Trend | 118 |
| (empty) | 13 |

| Rating | Rows | Share |
|---|---:|---:|
| 5 | 12,534 | 55% |
| 4 | 4,908 | 22% |
| 3 | 2,823 | 12% |
| 2 | 1,548 | 7% |
| 1 | 821 | 4% |

## Things to know

- **Only people who wrote a review are here.** Customers chose to review, and most were happy: 77% gave 4 or 5 stars. These counts describe this dataset, not all customers or all items.
- **Ratings skew positive.** A rule that always predicts "4 or 5 stars" is right 77% of the time. Compare any method with that baseline.
- **`recommended` and `rating` are related but not the same.** 82% of reviewers recommend the item. Most 4- and 5-star reviews recommend the item, and most 1- and 2-star reviews do not. But there are exceptions: 109 reviews with 1–2 stars recommend the item, and 187 with 4–5 stars do not. A 3-star review is a near coin flip (1,170 recommend, 1,653 do not).
- **Short, informal text.** Reviews have 2 to 115 words (median 59). Expect typos, abbreviations such as "tts" (true to size), sizes, heights and weights.
- **Lowercase after the first letter.** In the source file, every review is in lowercase except its first character.
- **Long reviews were cut by the source.** No review is longer than 508 characters. Reviews of about 500 characters (3,218 of them) often stop in the middle of a word or sentence.
- **Titles are often missing.** 2,965 reviews (13%) have no title. Use `review_text` for analysis.
- **Category spelling.** The source spells one division `Initmates`. It means Intimates; we kept the original spelling. The 13 reviews without a department also have no division and no class.
- **`age` is not checked.** It is the age in the source file. Treat it with care, and do not use it to describe groups of customers without saying so.
- **No names.** The source replaced the store's name with the word "retailer" (it appears in 2,014 reviews). The file holds no customer names or account IDs. Some reviews mention brand names of clothing labels.
- **Do not try to identify the people who wrote these reviews.**

## Source and license

- **Source:** *Women's E-Commerce Clothing Reviews*, published on Kaggle by nicapotato (`nicapotato/womens-ecommerce-clothing-reviews`): real, anonymized reviews from an unnamed online women's clothing retailer, 23,486 rows.
- **License:** the Kaggle page lists CC0 1.0 Universal (public domain dedication), as the OpenML and Hugging Face copies of the listing show. You may copy, change and share the data without asking permission. The course still names the source.
- **Our copy:** a Hugging Face mirror of the Kaggle file, cross-checked against a second mirror and OpenML dataset 43673 (also listed as CC0).

## How the course file was built

1. Renamed the columns (for example `Review Text` → `review_text`, `Recommended IND` → `recommended`) and kept the source row number as `review_id`.
2. Removed the 845 rows without review text.
3. Removed 7 reviews whose text exactly repeated an earlier review (the first copy was kept). 22,634 reviews remain.
4. Split the reviews 60/20/20 into `train`, `valid` and `test`, separately within each star rating (random seed 6403), so every split has the same rating mix.

The build script is kept by the instructor. SHA-256 of `clothing_reviews.csv`: `8a61265cd4b1421c95949affbc20acb39bbbbb44748daca78b11a076262e8682`. Sentence embeddings for every review are in `data/embeddings/clothing_minilm.npy` (see `data/embeddings/README.md`).
