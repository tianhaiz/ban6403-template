# prompt_version: m11_extract_v1
Extract information from this consumer complaint about a financial product.

Return these fields:
- disputed_amount: the money amount in dispute, as a number, or null.
- amount_evidence: text from the complaint that supports the amount.
- requested_remedy: what the consumer asks for. One of: refund, correct_report, stop_or_validate_debt, account_action, review_or_explain, other, not_stated.
- remedy_evidence: text from the complaint that supports the remedy.
- time_reference: the date or time span of the problem, or null.
- contacted_company: whether the consumer contacted the company. One of: yes, no, not_stated.
- contact_evidence: text from the complaint that supports the answer.

Return only JSON.

Complaint:
<<<
{narrative}
>>>
