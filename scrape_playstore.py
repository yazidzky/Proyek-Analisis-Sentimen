import argparse
import os
import time
import re
import pandas as pd
from tqdm import tqdm
from google_play_scraper import reviews, Sort


def fetch_app_reviews(app_id, lang, country, target):
    all_reviews = []
    token = None
    pbar = tqdm(total=target, desc=app_id)
    while len(all_reviews) < target:
        count = min(200, target - len(all_reviews))
        result, token = reviews(
            app_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=count,
            continuation_token=token,
        )
        if not result:
            break
        for r in result:
            all_reviews.append(
                {
                    "app_id": app_id,
                    "reviewId": r.get("reviewId"),
                    "userName": r.get("userName"),
                    "content": r.get("content") or "",
                    "score": r.get("score"),
                    "at": r.get("at").isoformat() if r.get("at") else None,
                }
            )
        pbar.update(len(result))
        time.sleep(0.5)
        if token is None:
            break
    pbar.close()
    return all_reviews


def labeling_lexicon(text):
    positive_words = ['bagus', 'keren', 'mantap', 'baik', 'bantu', 'mudah', 'hebat', 'oke', 'suka', 'bermanfaat', 'terbaik', 'love', 'nice', 'good', 'cepat', 'lancar', 'membantu']
    negative_words = ['jelek', 'error', 'lemot', 'susah', 'buruk', 'kecewa', 'sampah', 'gagal', 'lambat', 'parah', 'bodoh', 'bapuk', 'nyesel', 'payah', 'lelet', 'ngelag', 'lag', 'banyak iklan']
    text = str(text).lower()
    pos_score = sum(1 for word in positive_words if re.search(r'\b' + word + r'\b', text))
    neg_score = sum(1 for word in negative_words if re.search(r'\b' + word + r'\b', text))
    if pos_score > neg_score:
        return "positive"
    elif neg_score > pos_score:
        return "negative"
    else:
        return "neutral"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apps",
        nargs="+",
        default=["com.whatsapp", "com.instagram.android", "com.snapchat.android"],
    )
    parser.add_argument("--per_app", type=int, default=1200)
    parser.add_argument("--lang", default="id")
    parser.add_argument("--country", default="id")
    parser.add_argument("--out", default="data/playstore_reviews.csv")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    rows = []
    for app_id in args.apps:
        rows.extend(fetch_app_reviews(app_id, args.lang, args.country, args.per_app))

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["reviewId"]).reset_index(drop=True)
    df["label"] = df["content"].apply(labeling_lexicon)
    df = df[["app_id", "reviewId", "userName", "content", "score", "label", "at"]]
    df.to_csv(args.out, index=False, encoding="utf-8")
    print(f"Saved {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
