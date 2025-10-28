from transformers import pipeline

sentiment = pipeline("sentiment-analysis")

texts = [
    "I love Python, it's so simple!",
    "Rust is too complex for beginners.",
    "JavaScript frameworks change too often."
]

results = sentiment(texts)
for t, r in zip(texts, results):
    print(f"{t} --> {r['label']} ({r['score']:.2f})")


from textblob import TextBlob

texts = [
    "I love Python, it's so simple!",
    "Rust is too complex for beginners.",
    "JavaScript frameworks change too often."
]

for text in texts:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    sentiment = "POSITIVE" if polarity > 0 else "NEGATIVE" if polarity < 0 else "NEUTRAL"
    print(f"{text} --> {sentiment} ({polarity:.2f})")
