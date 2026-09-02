from datasets import load_dataset
import pandas as pd

# Load TweetEval sentiment dataset
dataset = load_dataset("tweet_eval", "sentiment")

# Convert to pandas DataFrames
train_df = pd.DataFrame(dataset['train'])
val_df = pd.DataFrame(dataset['validation'])
test_df = pd.DataFrame(dataset['test'])

# Save to CSV for inspection
train_df.to_csv("data/dummy/tweeteval_train.csv", index=False)
val_df.to_csv("data/dummy/tweeteval_val.csv", index=False)
test_df.to_csv("data/dummy/tweeteval_test.csv", index=False)

# Print sample data
print("Training set sample:")
print(train_df.head())
print("\nValidation set sample:")
print(val_df.head())
print("\nTest set sample:")
print(test_df.head())
print("\nLabel distribution (train):")
print(train_df['label'].value_counts())