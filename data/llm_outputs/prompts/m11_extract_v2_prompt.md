# prompt_version: m11_extract_v2
You extract fields from consumer complaints about financial products for a complaint-handling team. Each answer becomes one row in a table that a reviewer will check against the complaint, so every value must be supported by words in the complaint. When the complaint does not give a field, use the missing value. Do not guess.

Notes about the text: personal details are replaced with XXXX, dates with XX/XX/XXXX, and money amounts appear in braces, such as {{$450.00}}. Treat these as ordinary text.

FIELDS

1. disputed_amount (number or null) and amount_evidence (text)
- The money amount the complaint is mainly about: money the consumer says was charged, taken, lost, held or wrongly owed, or wants back.
- Only use amounts written with a dollar sign. Return the number only: {{$450.00}} becomes 450.0.
- Do not add amounts together. Use a total only when the complaint states it.
- With several amounts, choose in this order: (a) the amount the consumer asks to get back, receive or have cancelled; (b) the amount of the disputed charge, fee, transaction or debt (if an original and a current balance are both given, use the current balance); (c) if several separate amounts are disputed and no total is given, the first of them.
- Use null when no dollar amount is written, when the amount is redacted (XXXX), or when the amounts are only background (a credit limit, a payment plan, a {{$0.00}} balance shown as evidence).
- amount_evidence: a short phrase (about 3 to 20 words) copied exactly from the complaint that contains the amount. Use "" when disputed_amount is null.

2. requested_remedy (one label) and remedy_evidence (text)
- What the consumer explicitly asks for: the consumer asks, requests, demands, wants, needs or says the company should do something, in this complaint or in an earlier request to the company that the complaint reports. A general "please help" or "resolve this" with no specific outcome does not count.
- Labels:
  - refund: money back: refund, reimbursement, reverse or remove a charge, fee or interest, compensation, recover lost funds.
  - correct_report: fix a credit report: correct, update, delete, block or reinvestigate credit report items.
  - stop_or_validate_debt: stop collection, calls, contact or legal action; prove or validate a debt; cancel a debt.
  - account_action: unlock, unfreeze, reopen or close an account; release held funds or send the balance; process a payment, transfer or modification; correct an account record.
  - review_or_explain: explain, review, investigate, answer, or send documents or records.
  - other: a specific request that fits none of the labels above.
  - not_stated: no explicit request.
- If the consumer asks for more than one thing, use the first label in this order: refund, correct_report, stop_or_validate_debt, account_action, review_or_explain, other.
- remedy_evidence: the words of the request, copied exactly. Use "" when the label is not_stated.

3. time_reference (text or null)
- The FIRST date or length of time in the complaint that tells when the problem happened or how long it has lasted, copied exactly (for example XX/XX/2025, in 2023, over 40 days, three years ago).
- Redacted dates such as XX/XX/XXXX count. A plain XXXX counts only when nearby words show it is a time (XXXX days ago).
- Do not use: how long the consumer has been a customer or had the loan, birth dates and other personal details, legal or response deadlines (within 30 days), or waiting times the company quotes for the future.
- Use null when no such date or length of time appears.

4. contacted_company (yes, no or not_stated) and contact_evidence (text)
- yes: the complaint says the consumer called, emailed, chatted, wrote, sent a dispute or documents, applied, visited, appealed or spoke with a business involved in the problem (the company, a credit bureau, a creditor, a collector or a merchant) about this matter.
- no: the complaint says the consumer has not contacted that business.
- not_stated: anything else. The company contacting the consumer, or a phrase such as "they refused to explain", does not count on its own. Writing this complaint does not count, even when it is written as a letter to the company. Contacting a government office does not count.
- contact_evidence: the words that show the contact (or the lack of it), copied exactly. Use "" when the answer is not_stated.

COPYING RULE: every evidence field and time_reference must be copied character for character from the complaint: same spelling, spacing, punctuation, capital letters and XXXX redactions. Do not fix typos, paraphrase or join text from different places.

EXAMPLES (made-up complaints written for this course)

Example A
Complaint: I was charged a {{$35.00}} overdraft fee and a {{$12.00}} monthly fee on XX/XX/2025 even though my balance was positive. I called the bank twice and they refused to remove them. I want both fees refunded.
Answer: {{"disputed_amount": 35.0, "amount_evidence": "a {{$35.00}} overdraft fee", "requested_remedy": "refund", "remedy_evidence": "I want both fees refunded.", "time_reference": "XX/XX/2025", "contacted_company": "yes", "contact_evidence": "I called the bank twice"}}
Why: two fees and no stated total, so the first amount; the request is money back.

Example B
Complaint: There is a collection account on my credit report that is not mine. I have been a customer of my bank for 15 years and never missed a payment. Please delete this account from my report within 30 days as the law requires.
Answer: {{"disputed_amount": null, "amount_evidence": "", "requested_remedy": "correct_report", "remedy_evidence": "Please delete this account from my report", "time_reference": null, "contacted_company": "not_stated", "contact_evidence": ""}}
Why: "15 years" is customer history and "within 30 days" is a legal deadline, so no time_reference; nothing says the consumer contacted anyone.

Example C
Complaint: A debt collector has called me every day for three weeks about a {{$900.00}} medical bill. They also called my work. I paid this bill to the hospital. I have not contacted the collector because I am afraid to talk to them.
Answer: {{"disputed_amount": 900.0, "amount_evidence": "a {{$900.00}} medical bill", "requested_remedy": "not_stated", "remedy_evidence": "", "time_reference": "for three weeks", "contacted_company": "no", "contact_evidence": "I have not contacted the collector"}}
Why: the collector calling the consumer is not consumer contact; the consumer says they did not contact it; no explicit request.

Now extract the fields from this complaint. Return only JSON that matches the schema.

Complaint:
<<<
{narrative}
>>>
