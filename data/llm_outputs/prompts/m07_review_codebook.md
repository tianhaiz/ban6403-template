# M07 clothing review aspect codebook (version 1)

Used for the reviewed sample and for the cached LLM labels (prompt `m07_review_aspects_v1`) in Lab 7 Practice. The data are the Women's E-Commerce Clothing Reviews in `data/course/clothing_reviews.csv`. Only `review_text` is labeled. Titles are not used.

The business question: which product aspects go with low ratings and with "not recommended", in each department?

## What to label

For each review, list every aspect the writer gives an **opinion** about. Use each aspect at most once per review. Facts with no opinion are not mentions. "I am 5'4 and ordered a small" is a fact; "it runs small" is an opinion about fit.

## Aspects

| Aspect | Definition | Typical evidence |
|---|---|---|
| `fit_size` | How the garment fits the body and how its size compares with the usual size: runs small or large, too tight or loose, length, proportions, petite sizing. | "runs small", "fits true to size", "too short in the torso" |
| `fabric_quality` | The material and how the item is made: feel, thickness, sheerness, stitching, defects, durability, washing. | "the fabric is thin", "soft material", "came with a hole" |
| `style_look` | The design and how it looks on the wearer: cut, pattern, details, flattering or not, matches the photo (except color). | "so flattering", "looked like a maternity dress", "cute print" |
| `comfort` | How it feels to wear: comfortable, cozy, itchy, scratchy, restrictive, easy to move in. | "so comfortable", "itchy", "hard to move my arms" |
| `color` | The color or shade, including how it compares with the photo. | "the color is gorgeous", "much brighter than pictured" |
| `price_value` | Price, sale price and whether the item is worth the money. | "worth every penny", "too expensive for the quality" |

## Tie-break rules

1. Soft, thin, sheer, heavy or well made describe the material: `fabric_quality`. Comfortable, itchy, scratchy or cozy describe wearing it: `comfort`.
2. Too tight, too loose, too long or too short is `fit_size`. A shape that looks unflattering (boxy, frumpy, shapeless) is `style_look`.
3. "Runs small" or "size up" is a negative `fit_size` opinion, even when the writer then finds a size that fits. Then the tone is `mixed` if the writer also says the new size fits well.
4. A color that differs from the photo is `color`. A cut or pattern that differs from the photo is `style_look`.
5. Returning the item is an action, not an aspect. Label the reason for the return.

## Tone per aspect

- `positive`: the writer praises this aspect.
- `negative`: the writer criticizes this aspect.
- `mixed`: the writer both praises and criticizes this aspect (for example "the fabric is soft but wrinkles easily").

## Evidence span

Copy the shortest phrase (about 2 to 15 words) from the review that shows the aspect and its tone. Copy it exactly: same spelling, spacing, punctuation and lower-case letters. For a `mixed` aspect, copy the phrase with the criticism.

## Overall tone

The writer's verdict on the item as a whole:
- `positive`: mainly praise; small complaints are allowed when the writer still likes or keeps the item.
- `negative`: mainly criticism, or the writer returns or rejects the item.
- `mixed`: clear praise and clear criticism with no clear verdict ("it's okay", "love the color but it doesn't work on me").

## Notes about the text

About one review in five was cut off at about 500 characters in the source file, so it may end mid-word. Label what is there. The source replaced the company name with "retailer".

## Edge cases

This section was added after the second reading of the reviewed sample (October 15, 2026). It records how the final reviewed labels treat cases the rules above leave open. The cached LLM labels were made before it, with prompt `m07_review_aspects_v1`, which does not contain it.

1. **No verdict, no opinion.** There is no neutral overall label. A review with no opinion on any aspect and no clear verdict gets no aspect and overall `mixed` (review 116).
2. **Exchange for another size.** An exchange is not a rejection. If the writer praises the item and exchanges it for another size, the overall label is `mixed` (9780, 20514). If there is no praise, it is `negative` (15981).
3. **Kept, but with large complaints.** Keeping the item does not make the verdict positive when the complaints are large; use `mixed` (4385). A review that only reports a sizing problem, with no praise, is `negative` (3888, 5969).
4. **Tight versus uncomfortable.** Tightness that limits movement is `fit_size` (21258, "so tight in my shoulders i couldn't move my arms"). Irritation while wearing, such as a high collar that bothers the writer, is `comfort` (7495).
5. **Pattern or making defects.** A pattern printed or sewn off-center is a defect: `fabric_quality` (3238).
6. **Colors that run in the wash.** This is durability: `fabric_quality`, not `color` (13469).
7. **Shrinking after washing.** Also `fabric_quality` (22279).
8. **Implied sizing advice.** "Went with the small" after reading other reviews counts as "runs large": negative `fit_size` (2028).
9. **Color different from the picture or the name, without a stated feeling.** A difference from what the shopper expected is negative `color` (6226 "more cream than white", 11519). A shade described with positive words is positive (9118 "a very pale, soft pink").
10. **Cut-off reviews.** Label what is there, even if the span is cut off (10255 "it was much too", `mixed`). If the text stops before a verdict, the overall label is `mixed` (16967).
11. **Two colorways.** Label the review as a whole. If one colorway is praised and the other criticized for the same aspect, the aspect is `mixed` (19796, `fabric_quality`), and so is the overall label.
12. **One phrase for several aspects.** One span may serve as evidence for several aspects (14664 "comfortable and flattering"; 19796; 20514; 22697; 15182).
13. **Warmth and drape.** Warmth together with the feel of the material is `fabric_quality` (451 "very warm and soft"). Warmth as part of wearing it is `comfort` (9927 "comfortable, warm"). Drape as a property of the fabric is `fabric_quality` (13940 "the fabric is soft and stretchy, and it drapes well"). How the garment hangs and looks on the wearer is `style_look` (13970 "Loved how this draped").
