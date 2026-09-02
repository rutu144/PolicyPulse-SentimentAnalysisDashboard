import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO

def plot_sentiment_trends(df):
    # Aggregate sentiment by date
    sentiment_counts = df.groupby(['date', 'label']).size().unstack(fill_value=0)
    sentiment_counts = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100
    
    # Plot
    plt.figure(figsize=(10, 6))
    for label in sentiment_counts.columns:
        plt.plot(sentiment_counts.index, sentiment_counts[label], label=f"Label {label}")
    plt.legend(['Negative', 'Neutral', 'Positive'])
    plt.xlabel('Date')
    plt.ylabel('Percentage')
    plt.title('Sentiment Trends Over Time')
    
    # Save to base64
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def generate_wordcloud(texts):
    text = " ".join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save to base64
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64