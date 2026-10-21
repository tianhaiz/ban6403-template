"""Draw a reproducible project sample from the Yelp Open Dataset.

You download the Yelp Open Dataset yourself (you accept Yelp's terms on its
site). This script reads two of its files:

    yelp_academic_dataset_business.json   (about 120 MB)
    yelp_academic_dataset_review.json     (about 5 GB)

Both are JSON lines: one record per line. The script reads them line by line,
so it never needs the whole review file in memory. It keeps the reviews of
businesses in one city and one category, draws a fixed number of them with a
fixed seed, and writes:

    a CSV file: review_id, business_id, business_name, categories, city,
                state, stars, date, useful, funny, cool, n_words, text, split
    a manifest: filters, seed, counts and SHA-256 hashes (next to the CSV)

The reviewer ID (`user_id`) is dropped; reviewer names are never read (they
are only in the user file). The `split` column (train / valid / test, about
70 / 15 / 15 percent of reviews) keeps all reviews of one business in one
split.

The same files and settings always give the same sample, on any computer: a
review is chosen by a hash of the seed and its review ID, not by its position
in the file.

Run it from the Yelp starter notebook (Part 2), or from a terminal:

    python project_starters/yelp_sample.py --raw-dir project/data/private/yelp
    python project_starters/yelp_sample.py --raw-dir project/data/private/yelp --list-cities

The sample (about 15 MB for 20,000 reviews) goes to project/data/sample/. You
may commit it to your private course repository, so the instructor can rerun
your work. The two downloaded files stay in project/data/private/, which Git
ignores. Never publish the sample or review text (Yelp's terms).

Options: --city, --state, --category, --n, --seed, --start-date, --end-date,
--out. Run with --help for details. Uses only the Python standard library.
"""
import argparse
import csv
import hashlib
import heapq
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BUSINESS_FILE = "yelp_academic_dataset_business.json"
REVIEW_FILE = "yelp_academic_dataset_review.json"
DEFAULTS = {"city": "Philadelphia", "state": "PA", "category": "Restaurants", "n": 20000, "seed": 6403}
SPLIT_SHARES = (("train", 0.70), ("valid", 0.15), ("test", 0.15))
COLUMNS = ["review_id", "business_id", "business_name", "categories", "city", "state", "stars", "date",
           "useful", "funny", "cool", "n_words", "text", "split"]
BUSINESS_ID_PATTERN = re.compile(rb'"business_id"\s*:\s*"([^"]+)"')


def norm(value):
    """Compare names without case or extra spaces."""
    return " ".join(str(value or "").split()).casefold()


def seeded_key(seed, value):
    """A number fixed by the seed and the value, independent of file order."""
    return hashlib.sha256(f"{seed}:{value}".encode()).hexdigest()


def read_lines(path, hasher=None):
    """Yield the lines of a large file one at a time and update a SHA-256 hash."""
    with open(path, "rb") as handle:
        for line in handle:
            if hasher is not None:
                hasher.update(line)
            if line.strip():
                yield line


def category_list(record):
    return [c.strip() for c in (record.get("categories") or "").split(",") if c.strip()]


def load_businesses(path, city, state, category):
    """Return {business_id: business} for one city, state and category, plus the file hash."""
    hasher = hashlib.sha256()
    keep, n_all = {}, 0
    for line in read_lines(path, hasher):
        n_all += 1
        b = json.loads(line)
        if city and norm(b.get("city")) != norm(city):
            continue
        if state and norm(b.get("state")) != norm(state):
            continue
        if category and norm(category) not in {norm(c) for c in category_list(b)}:
            continue
        keep[b["business_id"]] = {"name": b.get("name", ""), "categories": b.get("categories") or "",
                                  "city": b.get("city", ""), "state": b.get("state", "")}
    return keep, n_all, hasher.hexdigest()


def list_cities(business_path, category, top=25):
    """Print the cities with the most businesses and reviews in a category."""
    counts = Counter()
    reviews = Counter()
    for line in read_lines(business_path):
        b = json.loads(line)
        if category and norm(category) not in {norm(c) for c in category_list(b)}:
            continue
        key = (" ".join(str(b.get("city") or "").split()).title(), str(b.get("state") or "").strip().upper())
        counts[key] += 1
        reviews[key] += int(b.get("review_count") or 0)
    print(f"Cities with the most '{category or 'any category'}' businesses (review_count is Yelp's total, "
          f"not the reviews in the file):")
    print(f"{'city':<28}{'state':<7}{'businesses':>11}{'review_count':>14}")
    for (city, state), n in counts.most_common(top):
        print(f"{city:<28}{state:<7}{n:>11,}{reviews[(city, state)]:>14,}")
    return counts


def sample_reviews(review_path, businesses, n, seed, start_date="", end_date=""):
    """Stream the review file; keep the n matching reviews with the smallest seeded keys."""
    hasher = hashlib.sha256()
    heap = []  # keeps the n smallest keys; the largest of them is on top
    n_lines = n_match = 0
    for line in read_lines(review_path, hasher):
        n_lines += 1
        found = BUSINESS_ID_PATTERN.search(line)
        if not found or found.group(1).decode() not in businesses:
            continue
        r = json.loads(line)
        day = str(r.get("date", ""))[:10]
        if (start_date and day < start_date) or (end_date and day > end_date):
            continue
        n_match += 1
        key = seeded_key(seed, r["review_id"])
        item = (_Inverse(key), r["review_id"], r)
        if len(heap) < n:
            heapq.heappush(heap, item)
        elif key < heap[0][0].key:
            heapq.heapreplace(heap, item)
    chosen = sorted(((entry[0].key, entry[2]) for entry in heap), key=lambda pair: pair[0])
    return [r for _, r in chosen], n_lines, n_match, hasher.hexdigest()


class _Inverse:
    """Wraps a key so that heapq (a min-heap) keeps the largest key on top."""
    __slots__ = ("key",)

    def __init__(self, key):
        self.key = key

    def __lt__(self, other):
        return self.key > other.key


def assign_splits(reviews, seed):
    """Put whole businesses into train, valid and test, about 70/15/15 percent of reviews.

    Businesses are taken from the most reviewed to the least reviewed (ties in a seeded
    random order). Each one goes to the split that is furthest below its target, relative
    to that target. Large businesses are then spread over the three splits, and small ones
    fill the gaps, so the shares come out close to 70/15/15.
    """
    per_business = Counter(r["business_id"] for r in reviews)
    order = sorted(per_business, key=lambda b: (-per_business[b], seeded_key(seed, "split:" + b)))
    total = len(reviews)
    target = {name: share * total for name, share in SPLIT_SHARES}
    filled = {name: 0 for name, _ in SPLIT_SHARES}
    split_of = {}
    for business_id in order:
        name = max(target, key=lambda s: (target[s] - filled[s]) / target[s])
        split_of[business_id] = name
        filled[name] += per_business[business_id]
    return split_of


def file_sha256(path):
    """SHA-256 of a text file, with Windows line endings counted as Unix ones (as in the starters)."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def make_sample(raw_dir, out, city=DEFAULTS["city"], state=DEFAULTS["state"], category=DEFAULTS["category"],
                n=DEFAULTS["n"], seed=DEFAULTS["seed"], start_date="", end_date="", quiet=False):
    """Draw the sample, write the CSV and the manifest, and return the manifest."""
    raw_dir, out = Path(raw_dir), Path(out)
    business_path, review_path = raw_dir / BUSINESS_FILE, raw_dir / REVIEW_FILE
    for path in (business_path, review_path):
        if not path.exists():
            raise FileNotFoundError(f"Not found: {path}. Download the Yelp Open Dataset, extract it, "
                                    f"and put the two JSON files in {raw_dir}.")
    say = (lambda *a: None) if quiet else print
    say(f"Reading businesses: {business_path.name}")
    businesses, n_business_lines, business_sha = load_businesses(business_path, city, state, category)
    say(f"  {len(businesses):,} businesses match city={city!r}, state={state!r}, category={category!r}")
    if not businesses:
        raise ValueError("No business matches these filters. Run with --list-cities to see the options.")
    say(f"Reading reviews (a few minutes for the full file): {review_path.name}")
    chosen, n_review_lines, n_match, review_sha = sample_reviews(review_path, businesses, n, seed,
                                                                 start_date, end_date)
    say(f"  {n_match:,} matching reviews; sample: {len(chosen):,}")
    if len(chosen) < n:
        say(f"  NOTE: fewer matching reviews than n={n:,}; the sample keeps all of them.")
    split_of = assign_splits(chosen, seed)

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        for r in sorted(chosen, key=lambda r: r["review_id"]):
            b = businesses[r["business_id"]]
            text = str(r.get("text") or "")
            writer.writerow({"review_id": r["review_id"], "business_id": r["business_id"],
                             "business_name": b["name"], "categories": b["categories"], "city": b["city"],
                             "state": b["state"], "stars": r.get("stars"), "date": r.get("date", ""),
                             "useful": r.get("useful", 0), "funny": r.get("funny", 0), "cool": r.get("cool", 0),
                             "n_words": len(text.split()), "text": text, "split": split_of[r["business_id"]]})

    split_reviews = Counter(split_of[r["business_id"]] for r in chosen)
    split_businesses = Counter(split_of.values())
    manifest = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "script": "project_starters/yelp_sample.py",
        "source": "Yelp Open Dataset (downloaded by the student under Yelp's dataset terms)",
        "filters": {"city": city, "state": state, "category": category,
                    "start_date": start_date or None, "end_date": end_date or None},
        "n_requested": n,
        "seed": seed,
        "selection": "the n matching reviews with the smallest sha256(seed:review_id)",
        "split_rule": "whole businesses, largest first (ties by sha256(seed:split:business_id)); each goes to the split furthest below its 70/15/15 percent target",
        "dropped_fields": ["user_id"],
        "counts": {
            "business_lines": n_business_lines, "matching_businesses": len(businesses),
            "review_lines": n_review_lines, "matching_reviews": n_match, "sampled_reviews": len(chosen),
            "sampled_businesses": len(split_of),
            "reviews_by_split": {s: split_reviews.get(s, 0) for s, _ in SPLIT_SHARES},
            "businesses_by_split": {s: split_businesses.get(s, 0) for s, _ in SPLIT_SHARES},
        },
        "input_files": [
            {"file": BUSINESS_FILE, "bytes": business_path.stat().st_size, "sha256": business_sha},
            {"file": REVIEW_FILE, "bytes": review_path.stat().st_size, "sha256": review_sha},
        ],
        "output": {"file": out.name, "sha256": file_sha256(out), "columns": COLUMNS},
    }
    manifest_path = out.with_name(out.stem + "_manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2))
    say(f"Wrote {out} and {manifest_path.name}")
    say(f"  reviews by split: {manifest['counts']['reviews_by_split']}")
    say(f"  businesses by split: {manifest['counts']['businesses_by_split']}")
    if min(split_businesses.get(s, 0) for s, _ in SPLIT_SHARES) < 20:
        say("  NOTE: a split has fewer than 20 businesses. Consider a larger city or category.")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description="Draw a reproducible sample from the Yelp Open Dataset.")
    parser.add_argument("--raw-dir", default="project/data/private/yelp",
                        help="folder with the two Yelp JSON files (default: %(default)s)")
    parser.add_argument("--out", default="project/data/sample/yelp_sample.csv",
                        help="CSV to write; the manifest goes next to it (default: %(default)s)")
    parser.add_argument("--city", default=DEFAULTS["city"], help="city (default: %(default)s)")
    parser.add_argument("--state", default=DEFAULTS["state"], help="state or province code (default: %(default)s)")
    parser.add_argument("--category", default=DEFAULTS["category"],
                        help="one Yelp category, such as Restaurants or 'Hotels & Travel' (default: %(default)s)")
    parser.add_argument("--n", type=int, default=DEFAULTS["n"], help="reviews to sample (default: %(default)s)")
    parser.add_argument("--seed", type=int, default=DEFAULTS["seed"], help="seed (default: %(default)s)")
    parser.add_argument("--start-date", default="", help="keep reviews on or after this date, YYYY-MM-DD")
    parser.add_argument("--end-date", default="", help="keep reviews on or before this date, YYYY-MM-DD")
    parser.add_argument("--quiet", action="store_true", help="print nothing")
    parser.add_argument("--list-cities", action="store_true",
                        help="only list the cities with the most businesses in the category")
    args = parser.parse_args(argv)
    if args.list_cities:
        list_cities(Path(args.raw_dir) / BUSINESS_FILE, args.category)
        return 0
    make_sample(args.raw_dir, args.out, args.city, args.state, args.category, args.n, args.seed,
                args.start_date, args.end_date, quiet=args.quiet)
    return 0


if __name__ == "__main__":
    sys.exit(main())
