# Support Inbox Data (practice data)

`support_messages.csv` holds 154 short customer messages sent to the support team of **Fernhollow Financial**, the bank behind the Module 12 help center (`data/rag/`). The bank, its policies and all the messages were written for this course. It is practice data, not a project data option.

## Columns

| Column | Meaning |
|---|---|
| `message_id` | Stable ID, `SUP001` to `SUP154`. Use it to link every output back to a message. |
| `channel` | `chat`, `secure_message` or `email` |
| `text` | The customer's message |
| `n_words` | Number of words in `text` |
| `topic` | The team that should handle the message (9 topics, see below). Security codes, phishing messages and Fraud Line hours belong to `fraud_scams`. A charge the customer does not recognize but asks to *dispute* belongs to `disputes`. |
| `answerable` | Can the help center answer it? `yes`; `partly` (it answers part of the question, or it gives general context on the same process without the specific answer, for example the card dispute process when the customer asks about business cards); `no` (no passage covers the process or object asked about) |
| `expected_source_ids` | The help passages that answer the message, separated by `;` (for example `KB05-1;KB05-2`). Empty when `answerable` is `no`. |
| `priority` | `urgent` when the customer is losing money now (fraud or a scam in progress, money just sent to the wrong person) or faces a deadline within days (access to money needed this week, a dispute or fraud window about to close); otherwise `routine`. A past loss, a payment due next month or a card that is already locked is `routine`. |
| `label_note` | Why a hard case got its labels. Empty for most messages. |
| `split` | `dev` (92 messages) or `test` (62). Do not change it. |

## Counts

| Topic | What it covers | dev | test |
|---|---|---:|---:|
| `account_services` | Sign-in, frozen or closed accounts, deposit holds, travel and account terms | 11 | 9 |
| `complaints_contact` | Complaints to the bank, contact hours and channels | 8 | 5 |
| `credit_reporting` | What the bank reports to credit bureaus, disputes, inquiries | 9 | 6 |
| `debt_collection` | Charged-off debts, validation, sold debts, settlements | 10 | 6 |
| `disputes` | Card disputes with merchants | 11 | 7 |
| `fees` | Overdraft, maintenance, late, wire and service fees | 12 | 9 |
| `fraud_scams` | Unauthorized transactions, scams, identity theft, security codes and phishing | 12 | 6 |
| `mortgage_escrow` | Mortgage payments, escrow, insurance, hardship | 11 | 8 |
| `payments_transfers` | QuickSend person-to-person payments and wires | 8 | 6 |
| **All** | | **92** | **62** |

- `answerable`: yes 117 (dev 69, test 48), partly 13 (8, 5), no 24 (15, 9).
- `priority`: urgent 11 (dev 8, test 3), routine 143.
- Messages are 5 to 31 words long (median 15).
- 107 answerable messages list one passage, 20 list two and 3 list three.

## How the file was made

- The messages were written for this course to cover every help article, in the styles of chat, secure messages and email. Some are short and informal; some give more detail.
- Some messages are hard on purpose. One asks to dispute a charge the customer does not recognize, which the help center sends to fraud reporting. One asks a question that the stale article KB03 answers wrongly. One asks about a fee charged under the archived fee schedule KB11. Some fit two topics. `label_note` explains these cases.
- About one message in six asks something the help center does not cover, such as accounts for minors, wire recalls, or foreign transaction fees.
- Draft labels were written with AI assistance and reviewed by the instructor. They were read against the help center before any search or model was run. A second reading checked every message and a third reading checked the harder ones. Disagreements were settled by majority or by the written rules above. They are not ground truth. Another careful reader may disagree on a few messages.
- The split was drawn once, at random within each topic, with seed 6403: about 60% `dev` and 40% `test`. Labels corrected after the draw (SUP064 and the label review) kept the split.
- No test message repeats or rewords one of the 20 Lab 12 questions (`data/rag/m12_questions.csv`). Some dev messages ask about the same topics as Lab 12, so a method built in Lab 12 may already fit them. That is one more reason to score `test` only once.

## How to use it

- Build and tune on `dev`. If your method has settings, choose them on one fixed half of `dev` and check them once on the other half. Score `test` once, after you freeze your method.
- Search the whole help center (`data/rag/m12_kb_passages.csv`); it is not split.
- Message embeddings are not included. The Module 12 passage embeddings (`data/embeddings/m12_passages_minilm.npy`) are.
- You may correct a `dev` label if you document the change and the reason. Never change `test` labels after you have seen results.

## File fingerprints (SHA-256, first 12 characters)

| File | SHA-256 |
|---|---|
| `data/support/support_messages.csv` | `63a6ad4e20a9` |
| `data/rag/m12_kb_passages.csv` | `d9d1bc3ef1e4` |
| `data/rag/m12_kb_articles.csv` | `46bfece3916a` |

Do not edit these files; save your own outputs in `outputs/`.
