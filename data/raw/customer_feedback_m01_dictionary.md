# M01 customer feedback: data dictionary

Original synthetic course fixture, 24 messages. Fictional electronics business. No personal information, actual transactions, real customers, timestamps, or observed service outcomes. Preserve all rows and IDs.

| Field | Meaning | Caution |
|---|---|---|
| feedback_id | Stable message ID, FB001–FB024 | A message ID is not a customer ID. |
| channel | review, email, or chat | Equal channel counts were deliberately constructed; no population inference. |
| product | speaker, headset, or tablet | Fictional product categories. |
| stars | Integer 1–5 | An illustrative overall-experience rating captured with each message, including email/chat; not every real channel provides ratings. Not an action-needed label. |
| text | Captured message | One missing value, duplicated text, and ambiguous wording are intentional. |

M01 uses this file to read cases and frame a decision. The initial review policy is an explicit unresolved issue or request for help. Unclear messages require additional evidence. Author-created slide interpretations do not establish customer outcomes. M02 will revisit source coverage and label policy on the same IDs. Later modeling labs require a larger approved corpus; this tiny file cannot justify reported classifier performance.
