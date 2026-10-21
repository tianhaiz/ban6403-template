# Course Dataset: CFPB Consumer Complaints

> This folder holds two course datasets. `cfpb_complaints.csv` (this page) is the main lab data, used from Module 1 on. `clothing_reviews.csv`, 22,634 reviews from a women’s clothing store, is the Practice data for Modules 4, 5 and 7; its data card is `clothing_reviews_README.md`.

`cfpb_complaints.csv` holds 10,000 real complaints that consumers sent to the U.S. Consumer Financial Protection Bureau (CFPB) between July and December 2025. Each row is one complaint, written by the consumer.

## Columns

| Column | Meaning |
|---|---|
| complaint_id | CFPB's ID for the complaint. Use it to link outputs back to the text. |
| date_received | Date CFPB received the complaint |
| product | Product the consumer chose (6 products, see below) |
| sub_product, issue, sub_issue | More detail the consumer chose |
| narrative | The complaint in the consumer's own words |
| company | Company the complaint is about |
| state | Consumer's state |
| submitted_via | How it was submitted (web, referral, ...) |
| company_response | How the company closed the complaint |
| timely_response | Whether the company replied on time |
| split | `train` (6,000), `valid` (2,000) or `test` (2,000). Do not change it. |

| Product | Rows |
|---|---:|
| Credit reporting or other personal consumer reports | 2,500 |
| Debt collection | 2,000 |
| Checking or savings account | 1,500 |
| Credit card | 1,500 |
| Money transfer, virtual currency, or money service | 1,250 |
| Mortgage | 1,250 |

## Things to know

- **Redactions.** CFPB replaces names and other personal details with `XXXX`. Dates appear in two main forms: `XX/XX/XXXX` (in 2,564 narratives) and `XX/XX/year>` (in 2,755 narratives). Both mean a hidden date. A few other forms, such as `XX/XX/2025`, are rare. Money amounts appear in braces, such as `{$450.00}`.
- **Not a random sample of customers.** Only people who chose to complain are here. We also set the number of rows per product, so these counts do not show how common each problem is.
- **Length.** Every narrative has 30 to 600 words. Very short and very long complaints were left out.
- **Repeated letters.** Many complaints, especially about credit reports, are copies of the same template letter. No two narratives in the extract are exactly the same. But some letters still share their opening: 247 complaints share their first 100 characters with at least one other complaint (73 different openings). Module 2 (step 2.7) shows how to find them.
- **Repeated letters stay in one split.** Within each product, complaints with the same opening are in the same split. So a test complaint does not start like a training letter of the same product. Three openings appear under two or three products, and those sit in different splits. The largest of the three is a 14-complaint letter: 7 mortgage complaints in `test`, and 4 credit card and 3 credit reporting complaints in `train`. These 23 complaints are 0.2% of the data. They remain a leakage risk; these counts alone do not show how much they affect evaluation scores. The splits are kept as they are.
- **The product label is the consumer's choice.** It is usually right but not always.
- **Source.** CFPB stopped publishing new complaint narratives in August 2026. This data comes from CFPB's official narrative archive: https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/
- Complaints with profanity or insults were left out.
- Do not try to identify the people who wrote these complaints.

## Near-duplicate complaints (known limitation)

The opening check above finds only letters that start the same way. Some letters also repeat with a different opening. We measured this with TF-IDF word and word-pair vectors and cosine similarity of 0.95 or more.

- 230 pairs involve 177 of the 10,000 complaints. Most are credit reporting and debt collection letters.
- 78 pairs cross splits. They touch 18 of the 2,000 validation complaints and 14 of the 2,000 test complaints.
- This is under 1% of each held-out split. It changes the reported scores by well under one point, so the splits are kept as they are.

`cfpb_near_duplicates.csv` lists every pair: `complaint_id_a`, `complaint_id_b`, both splits, the cosine value and `cross_split`. For a project, you can drop or group these pairs before you split your own data. Module 2 (steps 2.7–2.8) shows why repeated text matters for a split and how to check openings. Lab 8 (step 2.2) explains leakage.
