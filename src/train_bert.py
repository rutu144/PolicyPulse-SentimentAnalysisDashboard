import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from src.preprocessing import preprocess_text

# Load and prepare dataset
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    # Check if cleaned_text exists; if not, preprocess the text column
    if 'cleaned_text' not in df.columns:
        if 'text' in df.columns:
            df['cleaned_text'] = df['text'].apply(preprocess_text)
        else:
            raise ValueError("Input CSV must contain either 'cleaned_text' or 'text' column")
    
    return df[['cleaned_text', 'label']].dropna()

# Convert to Hugging Face Dataset
def prepare_dataset(df):
    dataset = Dataset.from_pandas(df)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    def tokenize_function(examples):
        return tokenizer(examples['cleaned_text'], padding="max_length", truncation=True, max_length=128)
    
    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    tokenized_dataset = tokenized_dataset.rename_column("label", "labels")
    tokenized_dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'labels'])
    return tokenized_dataset

# Compute metrics
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train_bert(file_path="data/processed/preprocessed_tweeteval.csv"):
    # Load data
    df = load_data(file_path)
    
    # Split into train and validation
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Convert to Hugging Face Dataset
    train_dataset = prepare_dataset(train_df)
    val_dataset = prepare_dataset(val_df)
    
    # Initialize model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="models/bert_sentiment",
        eval_strategy="epoch",  # Updated from evaluation_strategy
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )
    
    # Train model
    trainer.train()
    
    # Save model
    trainer.save_model("models/bert_sentiment")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokenizer.save_pretrained("models/bert_sentiment")
    
    # Evaluate
    eval_results = trainer.evaluate()
    print(f"Validation Accuracy: {eval_results['eval_accuracy']:.4f}")
    
    return model, tokenizer

if __name__ == "__main__":
    # Use preprocessed dummy data
    model, tokenizer = train_bert("data/dummy/preprocessed_dummy_tweets.csv")