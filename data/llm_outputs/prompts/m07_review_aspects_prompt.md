# prompt_version: m07_review_aspects_v1
You label online customer reviews of women's clothing for a business analytics course.

Task: read ONE review. List every product aspect the writer gives an opinion about, and give the overall tone.

For each aspect mention return:
- aspect: one label from the list below. Use each aspect at most once.
- sentiment: "positive", "negative" or "mixed" toward that aspect. Use "mixed" when the writer both praises and criticizes the same aspect.
- evidence_span: the shortest phrase (about 2 to 15 words) copied EXACTLY from the review that shows this aspect and its sentiment. Copy character for character, including lower-case letters and punctuation. Do not paraphrase. For a mixed aspect, copy the phrase with the criticism.

Aspect labels:
- fit_size: how the garment fits the body and how its size compares with the usual size: runs small or large, too tight or loose, length, proportions, petite sizing.
- fabric_quality: the material and how the item is made: feel, thickness, sheerness, stitching, defects, durability, washing.
- style_look: the design and how it looks on the wearer: cut, pattern, details, flattering or not, matches the photo (except color).
- comfort: how it feels to wear: comfortable, cozy, itchy, scratchy, restrictive, easy to move in.
- color: the color or shade, including how it compares with the photo.
- price_value: price, sale price and whether the item is worth the money.

Rules:
- Only opinions count. A plain fact such as "I am 5'4 and ordered a small" is not a mention.
- Soft, thin, sheer, heavy or well made describe the material: fabric_quality. Comfortable, itchy, scratchy or cozy describe wearing it: comfort.
- Too tight, too loose, too long or too short is fit_size. A shape that looks unflattering (boxy, frumpy, shapeless) is style_look.
- "Runs small" or "size up" is a negative fit_size opinion, even when the writer then finds a size that fits. If the writer also says the new size fits well, use "mixed".
- Returning the item is an action, not an aspect. Label the reason for the return.
- If no aspect fits, return an empty list.

overall_sentiment: the writer's verdict on the item as a whole.
- "positive": mainly praise; small complaints are allowed when the writer still likes or keeps the item.
- "negative": mainly criticism, or the writer returns or rejects the item.
- "mixed": clear praise and clear criticism with no clear verdict.

Some reviews were cut off in the source file and end mid-word. The company name was replaced by "retailer".

Return only JSON that matches the schema.

Review:
<<<
{review_text}
>>>
