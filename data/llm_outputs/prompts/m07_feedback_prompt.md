# prompt_version: m07_feedback_aspects_v1
You label short customer messages about a small electronics shop (speakers, headsets, tablets) for a business analytics course.

Task: read ONE message. List every product or service aspect the message gives an opinion or report about, and give the overall sentiment.

For each aspect mention return:
- aspect: one label from the list below.
- sentiment: "positive", "negative" or "neutral" toward that aspect. Use "neutral" for a plain question or a fact with no opinion.
- evidence_span: the words copied EXACTLY from the message that show this aspect and sentiment. Copy character for character. Do not paraphrase.

Aspect labels:
- device_performance: how the device works: sound, screen, battery life, starting up, comfort, setup.
- accessories: chargers, cables, ear cushions and other parts, including missing parts.
- delivery: shipping, arrival, lost or late packages.
- billing_refund: charges, bills, refunds, returns.
- support_service: help from staff, replacements, troubleshooting, case handling.
- appearance: color, look, match with the product photo.

If no aspect fits, return an empty list. Do not invent aspects that the message does not mention.

overall_sentiment: "positive", "negative", "mixed" (both positive and negative opinions) or "neutral" (no opinion).

Return only JSON that matches the schema.

Message:
<<<
{text}
>>>
