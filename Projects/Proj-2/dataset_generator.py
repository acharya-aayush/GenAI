import csv
import random
import argparse
import os
import string

POSITIVE_ADJS = ["great", "excellent", "amazing", "fantastic", "wonderful", "lovely", "pleasant", "awesome", "perfect"]
NEGATIVE_ADJS = ["bad", "terrible", "awful", "horrible", "poor", "disappointing", "annoying", "worst", "lousy"]
NEUTRAL_ADJS = ["okay", "fine", "average", "normal", "acceptable", "mediocre"]

NOUNS = ["flight", "service", "crew", "plane", "seat", "delay", "bag", "staff", "experience", "pilot"]

EMOJIS = ["😀","😃","😄","😁","😅","😂","🙂","🙁","😡","😢","👍","👎","✈️","🔥"]
EMOTICONS = [":)", ":D", ":(", ":/", ";)", ":-)", ":-(" ]

SHORT_FORMS = {
    "you": "u",
    "are": "r",
    "please": "pls",
    "people": "ppl",
    "thanks": "thx",
    "because": "cuz",
    "okay": "ok",
    "really": "rly",
    "great": "gr8",
}

STOPWORDS = ["like", "actually", "basically", "literally", "just", "really", "so", "well"]


def random_typo(word):
    if len(word) <= 1:
        return word
    op = random.choice(["swap", "delete", "dup", "replace"]) 
    if op == "swap":
        i = random.randint(0, len(word) - 2)
        lst = list(word)
        lst[i], lst[i+1] = lst[i+1], lst[i]
        return "".join(lst)
    if op == "delete":
        i = random.randint(0, len(word) - 1)
        return word[:i] + word[i+1:]
    if op == "dup":
        i = random.randint(0, len(word) - 1)
        return word[:i] + word[i] + word[i:]
    if op == "replace":
        i = random.randint(0, len(word) - 1)
        repl = random.choice(string.ascii_lowercase)
        return word[:i] + repl + word[i+1:]


def maybe_misspell(word):
    # common simple misspells
    subs = {"good": "gud", "love": "luv", "flight": "flite", "service": "servce", "seat": "seet"}
    if word.lower() in subs and random.random() < 0.7:
        return subs[word.lower()]
    # small chance of adding a random typo
    if random.random() < 0.15:
        return random_typo(word)
    return word


def apply_short_forms(word):
    lw = word.lower()
    if lw in SHORT_FORMS and random.random() < 0.6:
        # keep case of first letter
        sf = SHORT_FORMS[lw]
        return sf
    return word


def random_punctuations():
    extras = ["!", "!!", "!!!", "..", ".", "???", "?!", "...", "-", "~"]
    return random.choice(extras)


def build_review(sentiment):
    # construct a base sentence
    noun = random.choice(NOUNS)
    if sentiment == "positive":
        adj = random.choice(POSITIVE_ADJS)
    elif sentiment == "negative":
        adj = random.choice(NEGATIVE_ADJS)
    else:
        adj = random.choice(NEUTRAL_ADJS)

    templates = [
        f"The {noun} was {adj}",
        f"{adj.capitalize()} {noun}",
        f"I found the {noun} {adj}",
        f"{noun.capitalize()} {adj} and the staff was {random.choice(POSITIVE_ADJS if sentiment== 'positive' else NEGATIVE_ADJS)}",
        f"{adj.capitalize()} experience with the {noun}",
    ]
    text = random.choice(templates)

    # add some filler stopwords randomly
    if random.random() < 0.4:
        text = text + " " + random.choice(STOPWORDS)

    words = text.split()

    out_words = []
    for w in words:
        clean = w.strip(string.punctuation)
        punct_before = "" if w[0].isalnum() else w[0]
        punct_after = "" if w[-1].isalnum() else w[-1]

        # apply short forms
        if random.random() < 0.2:
            clean = apply_short_forms(clean)

        # misspell sometimes
        clean = maybe_misspell(clean)

        # random typo on some words
        if random.random() < 0.12:
            clean = random_typo(clean)

        # randomly add extra punctuation
        if random.random() < 0.1:
            punct_after = punct_after + random_punctuations()

        out = punct_before + clean + punct_after
        out_words.append(out)

    review = " ".join(out_words)

    # randomly append emojis or emoticons
    if random.random() < 0.35:
        review = review + " " + random.choice(EMOJIS)
    if random.random() < 0.2:
        review = review + " " + random.choice(EMOTICONS)

    # randomly add elongated characters or interjections
    if random.random() < 0.12:
        review = review + " " + random.choice(["soooo", "looool", "omg", "wtf"]) 

    # random uppercasing for emphasis
    if random.random() < 0.05:
        review = review.upper()

    return review


def generate_reviews(n=1000, out_path="synthetic_reviews.csv"):
    sentiments = ["positive"] * 45 + ["negative"] * 45 + ["neutral"] * 10
    rows = []
    for _ in range(n):
        s = random.choice(sentiments)
        review = build_review(s)
        rows.append((review, s))

    # write CSV
    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["review", "sentiment"])
        writer.writerows(rows)

    return out_path


def print_preview(csv_path, k=10):
    print(f"\nSaved synthetic data to: {csv_path}\nFirst {k} rows:\n")
    with open(csv_path, encoding='utf-8') as f:
        for i, line in enumerate(f):
            print(line.strip())
            if i >= k:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate synthetic reviews')
    parser.add_argument('-n', type=int, default=1000, help='number of reviews to generate')
    parser.add_argument('--out', type=str, default='synthetic_reviews.csv', help='output CSV path')
    args = parser.parse_args()

    out = generate_reviews(n=args.n, out_path=args.out)
    # print first 10 rows
    print_preview(out, k=10)
