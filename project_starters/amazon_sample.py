"""Draw a reproducible project sample from one category of Amazon Reviews 2023.

You download one category of Amazon Reviews 2023 (McAuley Lab) yourself, for
example the review file All_Beauty.jsonl.gz and, if you want product names,
its metadata file meta_All_Beauty.jsonl.gz. Both are gzipped JSON lines: one
record per line. The script reads them line by line, so a large file never
has to fit in memory. It draws a fixed number of reviews with a fixed seed and
writes:

    a CSV file: review_id, parent_asin, asin, product_title, rating, title,
                text, date, helpful_vote, verified_purchase, n_words, split
    a manifest: settings, seed, counts and SHA-256 hashes (next to the CSV)

Only reviews with at least --min-words words of text (default 50) are kept.
Words are counted after HTML tags such as <br /> are removed. Why a minimum?
Most Amazon reviews are very short. We measured three small categories on
October 15, 2026 (full files from Hugging Face):

    category                  reviews   median words   50+ words   reviews left
    All_Beauty                701,528        19            19%         131,499
    Health_and_Personal_Care  494,121        20            21%         102,328
    Handmade_Products         664,162        17            12%          81,611

A review such as "Great product, works well" gives a method and a human
labeler almost nothing to work with. The filter keeps reviews that describe
something and still leaves far more reviews than the 20,000 you sample. Short
reviews are not a random subset: they lean more toward 5 stars. Use
--min-words 0 to keep all reviews, or another value, and say in your README
which value you used and why.

The reviewer ID (`user_id`) and the image links are dropped. The files have no
review ID, so the script builds one: a short hash of the reviewer ID, product
and time. Some reviews appear twice in the files; the sample keeps one copy. The hash cannot be turned back into the reviewer ID. The `split`
column (train / valid / test, about 70 / 15 / 15 percent of reviews) keeps all
reviews of one product (`parent_asin`) in one split.

The same files and settings always give the same sample, on any computer.

Run it from the Amazon starter notebook (Part 2), or from a terminal:

    python project_starters/amazon_sample.py --reviews project/data/private/amazon/All_Beauty.jsonl.gz \
        --meta project/data/private/amazon/meta_All_Beauty.jsonl.gz

The review file may be gzipped (.jsonl.gz, from the project page) or not
(.jsonl, from Hugging Face). The sample (about 10 to 15 MB for 20,000 reviews)
goes to project/data/sample/, which you commit to your private course
repository; the downloaded files stay in project/data/private/.

Options: --n, --seed, --min-words, --start-date, --end-date, --out. Run with --help for
details. Uses only the Python standard library.
"""
import argparse
import csv
import gzip
import hashlib
import heapq
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DEFAULTS = {"n": 20000, "seed": 6403, "min_words": 50}
SPLIT_SHARES = (("train", 0.70), ("valid", 0.15), ("test", 0.15))
COLUMNS = ["review_id", "parent_asin", "asin", "product_title", "rating", "title", "text", "date",
           "helpful_vote", "verified_purchase", "n_words", "split"]


TAG = re.compile(r"<[^>]+>")


def count_words(text):
    """Words in a review text, after HTML tags such as <br /> are removed."""
    return len(TAG.sub(" ", str(text or "")).split())


def seeded_key(seed, value):
    """A number fixed by the seed and the value, independent of file order."""
    return hashlib.sha256(f"{seed}:{value}".encode()).hexdigest()


def read_lines(path, hasher=None):
    """Yield the lines of a .jsonl or .jsonl.gz file and update a SHA-256 hash of the file bytes."""
    path = Path(path)
    if hasher is not None:
        with open(path, "rb") as raw:
            for block in iter(lambda: raw.read(1 << 20), b""):
                hasher.update(block)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as handle:
        for line in handle:
            if line.strip():
                yield line


class _Inverse:
    """Wraps a key so that heapq (a min-heap) keeps the largest key on top."""
    __slots__ = ("key",)

    def __init__(self, key):
        self.key = key

    def __lt__(self, other):
        return self.key > other.key


def review_id(r):
    raw = f"{r.get('user_id', '')}|{r.get('asin', '')}|{r.get('timestamp', '')}"
    return "R" + hashlib.sha256(raw.encode()).hexdigest()[:15]


def to_date(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp) / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError, OSError):
        return ""


def sample_reviews(path, n, seed, start_date="", end_date="", min_words=0):
    hasher = hashlib.sha256()
    heap, n_lines, n_match, n_short, n_repeat = [], 0, 0, 0, 0
    in_heap = set()
    for line in read_lines(path, hasher):
        n_lines += 1
        r = json.loads(line)
        day = to_date(r.get("timestamp"))
        if (start_date and day < start_date) or (end_date and day > end_date):
            continue
        if count_words(r.get("text")) < min_words:
            n_short += 1
            continue
        n_match += 1
        r["_id"], r["_date"] = review_id(r), day
        key = seeded_key(seed, r["_id"])
        item = (_Inverse(key), r["_id"], r)
        if len(heap) < n or key < heap[0][0].key:
            if r["_id"] in in_heap:
                # The files repeat some reviews (same reviewer, product and time): keep the first copy.
                n_repeat += 1
                continue
            in_heap.add(r["_id"])
            if len(heap) < n:
                heapq.heappush(heap, item)
            else:
                in_heap.discard(heapq.heapreplace(heap, item)[1])
    return [entry[2] for entry in heap], n_lines, n_match, n_short, n_repeat, hasher.hexdigest()


def product_titles(meta_path, wanted):
    titles = {}
    for line in read_lines(meta_path):
        m = json.loads(line)
        if m.get("parent_asin") in wanted:
            titles[m["parent_asin"]] = m.get("title") or ""
    return titles


def assign_splits(reviews, seed, group="parent_asin"):
    """Whole products, largest first (ties in seeded order); each to the split furthest below its target."""
    per_group = Counter(r[group] for r in reviews)
    order = sorted(per_group, key=lambda g: (-per_group[g], seeded_key(seed, "split:" + g)))
    total = len(reviews)
    target = {name: share * total for name, share in SPLIT_SHARES}
    filled = {name: 0 for name, _ in SPLIT_SHARES}
    split_of = {}
    for g in order:
        name = max(target, key=lambda s: (target[s] - filled[s]) / target[s])
        split_of[g] = name
        filled[name] += per_group[g]
    return split_of


def file_sha256(path):
    """SHA-256 of a text file, with Windows line endings counted as Unix ones (as in the starters)."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def make_sample(reviews_path, out, meta_path="", n=DEFAULTS["n"], seed=DEFAULTS["seed"], start_date="",
                end_date="", quiet=False, min_words=DEFAULTS["min_words"]):
    """Draw the sample, write the CSV and the manifest, and return the manifest."""
    reviews_path, out = Path(reviews_path), Path(out)
    if not reviews_path.exists():
        raise FileNotFoundError(f"Not found: {reviews_path}. Download one category of Amazon Reviews 2023 "
                                f"and put the file there.")
    say = (lambda *a: None) if quiet else print
    say(f"Reading reviews: {reviews_path.name}")
    if min_words < 0:
        raise ValueError("min_words must be 0 or more.")
    chosen, n_lines, n_match, n_short, n_repeat, reviews_sha = sample_reviews(reviews_path, n, seed, start_date, end_date,
                                                                     min_words)
    if not chosen:
        raise ValueError("No review matches these settings.")
    say(f"  {n_lines:,} reviews in the file; {n_short:,} in the date range have fewer than {min_words} words")
    say(f"  {n_match:,} matching reviews; sample: {len(chosen):,} ({n_repeat:,} repeated copies skipped)")
    if len(chosen) < n:
        say(f"  NOTE: fewer matching reviews than n={n:,}; the sample keeps all of them.")
    titles, meta_record = {}, None
    if meta_path:
        meta_path = Path(meta_path)
        say(f"Reading product names: {meta_path.name}")
        titles = product_titles(meta_path, {r.get("parent_asin") for r in chosen})
        meta_record = {"file": meta_path.name, "bytes": meta_path.stat().st_size}
    for r in chosen:
        r["parent_asin"] = r.get("parent_asin") or r.get("asin", "")
    split_of = assign_splits(chosen, seed)

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        for r in sorted(chosen, key=lambda r: r["_id"]):
            text = str(r.get("text") or "")
            writer.writerow({"review_id": r["_id"], "parent_asin": r["parent_asin"], "asin": r.get("asin", ""),
                             "product_title": titles.get(r["parent_asin"], ""), "rating": r.get("rating"),
                             "title": r.get("title", ""), "text": text, "date": r["_date"],
                             "helpful_vote": r.get("helpful_vote", 0),
                             "verified_purchase": int(bool(r.get("verified_purchase"))),
                             "n_words": count_words(text), "split": split_of[r["parent_asin"]]})

    split_reviews = Counter(split_of[r["parent_asin"]] for r in chosen)
    split_products = Counter(split_of.values())
    manifest = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "script": "project_starters/amazon_sample.py",
        "source": "Amazon Reviews 2023, McAuley Lab (downloaded by the student; cite Hou et al., 2024)",
        "filters": {"start_date": start_date or None, "end_date": end_date or None, "min_words": min_words},
        "n_requested": n,
        "seed": seed,
        "selection": "the n matching reviews with the smallest sha256(seed:review_id); matching = in the date "
                     "range and at least min_words words of text (words = text split on white space after HTML tags are removed); "
                     "a repeated review (same review_id) is kept once",
        "review_id_rule": "R + first 15 hex characters of sha256(user_id|asin|timestamp)",
        "split_rule": "whole products (parent_asin), largest first (ties by sha256(seed:split:parent_asin)); "
                      "each goes to the split furthest below its 70/15/15 percent target",
        "dropped_fields": ["user_id", "images"],
        "counts": {"review_lines": n_lines, "too_short": n_short, "matching_reviews": n_match,
                   "repeated_reviews_skipped": n_repeat, "sampled_reviews": len(chosen),
                   "sampled_products": len(split_of),
                   "reviews_by_split": {s: split_reviews.get(s, 0) for s, _ in SPLIT_SHARES},
                   "products_by_split": {s: split_products.get(s, 0) for s, _ in SPLIT_SHARES},
                   "duplicate_review_ids": len(chosen) - len({r["_id"] for r in chosen})},
        "input_files": [{"file": reviews_path.name, "bytes": reviews_path.stat().st_size, "sha256": reviews_sha}]
                       + ([meta_record] if meta_record else []),
        "output": {"file": out.name, "sha256": file_sha256(out), "columns": COLUMNS},
    }
    manifest_path = out.with_name(out.stem + "_manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2))
    say(f"Wrote {out} and {manifest_path.name}")
    say(f"  reviews by split: {manifest['counts']['reviews_by_split']}")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description="Draw a reproducible sample from one Amazon Reviews 2023 category.")
    parser.add_argument("--reviews", required=True,
                        help="the category review file, such as All_Beauty.jsonl.gz or All_Beauty.jsonl")
    parser.add_argument("--meta", default="", help="the matching metadata file, for product names (optional)")
    parser.add_argument("--out", default="project/data/sample/amazon_sample.csv",
                        help="CSV to write; the manifest goes next to it (default: %(default)s)")
    parser.add_argument("--n", type=int, default=DEFAULTS["n"], help="reviews to sample (default: %(default)s)")
    parser.add_argument("--seed", type=int, default=DEFAULTS["seed"], help="seed (default: %(default)s)")
    parser.add_argument("--min-words", type=int, default=DEFAULTS["min_words"],
                        help="keep reviews with at least this many words of text; 0 keeps all (default: %(default)s)")
    parser.add_argument("--start-date", default="", help="keep reviews on or after this date, YYYY-MM-DD")
    parser.add_argument("--end-date", default="", help="keep reviews on or before this date, YYYY-MM-DD")
    parser.add_argument("--quiet", action="store_true", help="print nothing")
    args = parser.parse_args(argv)
    make_sample(args.reviews, args.out, args.meta, args.n, args.seed, args.start_date, args.end_date, args.quiet,
                args.min_words)
    return 0


if __name__ == "__main__":
    sys.exit(main())
