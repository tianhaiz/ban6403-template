# M11 Extraction Schema (version m11_schema_v1.2)

This schema turns one CFPB complaint into one table row. It is used for the reviewed labels, by the rule baseline and by prompt `m11_extract_v2`. Prompt `m11_extract_v1` names the same fields but leaves out most of these rules.

Version 1.1 adds one clarification to version 1: the sentence on requests addressed to the CFPB, marked below. Version 1.2 adds seven clarifications (marked *v1.2*) from the final label review in October 2026. Prompt `m11_extract_v2` was written from version 1 and contains none of them.

## Business use

A complaint-handling team wants a table that answers four questions for each complaint: how much money is at stake, what the consumer asks for, when the problem happened, and whether the consumer already tried the company. Every filled value must point back to words in the complaint, so a reviewer can check it in seconds.

## Fields

| Field | Type | Missing value | Evidence |
|---|---|---|---|
| `disputed_amount` | number (US dollars) | `null` | `amount_evidence` |
| `requested_remedy` | one label (see below) | `"not_stated"` | `remedy_evidence` |
| `time_reference` | text copied from the complaint | `null` | the value itself |
| `contacted_company` | `"yes"`, `"no"` or `"not_stated"` | `"not_stated"` | `contact_evidence` |

Evidence fields are text copied exactly from the complaint. They are the empty string `""` when the field is missing.

### 1. disputed_amount

The money amount the complaint is mainly about: money the consumer says was charged, taken, lost, held or wrongly owed, or wants back.

- Only use amounts written with a dollar sign. In this data they appear in braces, such as `{$450.00}`. Record the number only: `450.0`.
- Do not add amounts together. Use a total only when the complaint states it.
- *(v1.2)* If the consumer asks to get back or cancel two or more amounts, use the first one mentioned in the complaint.
- *(v1.2)* A list of account balances in a request to delete or block credit-report items is not a disputed amount. Use `null`, unless the consumer disputes one of those amounts itself (for example "I dispute a {$250.00} account").
- *(v1.2)* Money that the company holds or withholds counts (a held deposit, a held payment, a balance not returned). Payment amounts that are only background do not count (a monthly payment, a payment plan, a payment that was simply returned unpaid).
- When there are several amounts, choose in this order:
  1. the amount the consumer asks to get back, receive or have cancelled;
  2. the amount of the disputed charge, fee, transaction or debt (if an original and a current balance are both given, use the current balance);
  3. if several separate amounts are disputed and no total is given, the first of them.
- Use `null` when no dollar amount is written, when the amount is redacted (`XXXX`), or when the amounts are only background (a credit limit, a payment plan, a `{$0.00}` balance shown as evidence).
- `amount_evidence`: a short phrase (about 3 to 20 words) copied exactly from the complaint that contains the amount and shows what it is for.

### 2. requested_remedy

What the consumer explicitly asks for. A request counts when the consumer asks, requests, demands, wants, needs or says the company should do something, either in this complaint or in an earlier request to the company that the complaint reports. A general "please help" or "resolve this" with no specific outcome does not count. *(Added in v1.1.)* A request addressed to the CFPB counts only when it names a specific outcome for the consumer. Examples are a refund, a deletion or an end to collection. Asking the CFPB only to investigate, help, or take action against the company does not count.

*(v1.2)* A dispute, appeal or application that the consumer reports making earlier counts as a request, even when the complaint does not repeat the request. Label it by what the dispute, appeal or application asked for. A disputed charge is `refund`, and a disputed credit-report item is `correct_report`. A loan-modification or assistance application is `account_action`, and so is an appeal of an account closure.

| Label | Meaning |
|---|---|
| `refund` | Money back: refund, reimbursement, reverse or remove a charge, fee or interest, compensation, recover lost funds |
| `correct_report` | Fix a credit report: correct, update, delete, block or reinvestigate items on a credit report |
| `stop_or_validate_debt` | Stop collection, calls, contact or legal action; prove or validate a debt; cancel a debt |
| `account_action` | Act on an account: unlock, unfreeze, reopen or close it; release held funds or send the balance; process a payment, transfer or modification; correct an account record |
| `review_or_explain` | Explain, review, investigate, answer, or send documents or records |
| `other` | A specific request that fits none of the labels above |
| `not_stated` | No explicit request |

If the consumer asks for more than one thing, use the first label in this order: `refund`, `correct_report`, `stop_or_validate_debt`, `account_action`, `review_or_explain`, `other`.

*(v1.2)* Apply this order even when another request seems to be the main intent. For example, a request to prove a debt and to delete it from a credit report is `correct_report`.

`remedy_evidence`: the words of the request, copied exactly.

### 3. time_reference

The first date or length of time in the complaint that tells when the problem happened or how long it has lasted. Copy it exactly, for example `XX/XX/2025`, `in 2023`, `over 40 days`, `three years ago`.

- Redacted dates such as `XX/XX/XXXX` count. A plain `XXXX` counts only when nearby words show it is a time (for example `XXXX days ago`, `in XXXX of this year`).
- Do not use: how long the consumer has been a customer or had the loan, birth dates and other personal details, legal or response deadlines (`within 30 days`), and waiting times the company quotes for the future.
- *(v1.2)* The opening date of an account that the consumer says is fraudulent counts ("Date opened XX/XX/XXXX").
- *(v1.2)* `XX/XX/year>` is a redacted date and counts like `XX/XX/XXXX`.
- *(v1.2)* Skip dates that are only background to the problem (when an original contract ran, when funds were first deposited, how old an account is). Use the first date or length of time that belongs to the problem itself.
- Use `null` when no such date or length of time appears.

### 4. contacted_company

Did the consumer contact a business involved in the problem (the company complained about, a credit bureau, a creditor, a collector or a merchant) about this matter before the complaint?

- `yes`: the complaint says the consumer called, emailed, chatted, wrote, sent a dispute or documents, applied, visited, appealed or spoke with that business about the matter.
- `no`: the complaint says the consumer has not contacted the business.
- `not_stated`: anything else. The company contacting the consumer, or a phrase such as "they refused to explain", does not count on its own. Writing this complaint does not count, even when it is written as a letter to the company. Contacting a government office does not count. *(v1.2)* Contact that is only implied also counts as `not_stated`. Examples: "I could not get the issue resolved directly", "they refused to help" or "the company completed an investigation". The complaint must say that the consumer called, wrote, disputed, applied or visited.
- `contact_evidence`: the words that show the contact (or the lack of it), copied exactly.

## Validation rules (schema validity)

An output row is valid when all of these hold. Validity says nothing about whether the values are right.

1. All seven keys are present and have the right type; labels come from the allowed lists.
2. `disputed_amount` is `null` exactly when `amount_evidence` is `""`; otherwise the amount appears in `amount_evidence` in the `{$...}` form.
3. `requested_remedy` is `"not_stated"` exactly when `remedy_evidence` is `""`.
4. `contacted_company` is `"not_stated"` exactly when `contact_evidence` is `""`.
5. Every non-empty evidence field and `time_reference` appears exactly in the complaint text.

## Field correctness (compared with reviewed labels)

| Field | Counts as correct when |
|---|---|
| `disputed_amount` | both are `null`, or the numbers are equal (to the cent) |
| `requested_remedy` | the labels are the same |
| `time_reference` | both are `null`, or one text contains the other (ignoring extra spaces) |
| `contacted_company` | the labels are the same |

Error types: a **false extraction** fills a field that the reviewed label leaves missing; a **missing extraction** leaves a field missing that the reviewed label fills; a **wrong value** fills the field with a different value.
