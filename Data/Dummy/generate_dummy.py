# Save in data/dummy/generate_dummy.py
import pandas as pd

data = {
    "text": [
        "GST is killing small businesses with high rates",
        "Digital India is transforming rural areas with internet",
        "GST filing process is too complex for traders",
        "Digital India promotes e-governance, very efficient",
        "Neutral opinion on GST, needs simplification"
    ],
    "label": [0, 2, 0, 2, 1],
    "policy": ["GST", "Digital India", "GST", "Digital India", "GST"]
}
df = pd.DataFrame(data)
df.to_csv("data/dummy/dummy_tweets.csv", index=False)
print("Dummy dataset created.")