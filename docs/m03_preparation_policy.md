# Module 3 preparation policy: light_v1

**Use:** the 24 example messages and the CFPB complaint extract. Never change the raw files. Keep `feedback_id` (or `complaint_id`) with every prepared row.

**Choose rules on development data only.** For the example messages, use the 13 development IDs from Module 2. FB022 stays excluded (no text). FB005 and FB020 stay together in development. For CFPB complaints, use the `train` split.

**Light view (light_v1):** Unicode NFC, then split on whitespace and rejoin with single spaces. It keeps case, negation, punctuation, amounts and codes. It also joins line breaks, so do not use it where layout matters.

**Lowercase candidate:** the light view plus lowercase. It is a candidate for word-count features, not a better version.

**Not part of light_v1:** stopword removal, stemming, HTML stripping, spell correction, deleting redaction marks (`XXXX`). If you add a rule, put it in a new column and check what it changes.

**Test cases:** `data/raw/m03_preparation_test_cases.csv` holds six examples written for this lab (TC01–TC06). They show risks such as full-width characters (TC04), case (TC05) and line breaks (TC06). They are not customer data.

**What the lab saves:** a development audit (13 rows), the excluded-record list (1 row) and the test-case comparison (6 rows) in `outputs/m03`.
