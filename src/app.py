import sys
import os
from flask import Flask, render_template, request, send_file
import pandas as pd
import io

# Set project root and add to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import project modules
try:
    from src.theme_extraction import extract_themes
    from src.utils import plot_sentiment_trends, generate_wordcloud
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Set template and static directories
template_dir = os.path.join(project_root, 'templates')
static_dir = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Load preprocessed data
df = pd.read_csv(os.path.join(project_root, "data/dummy/preprocessed_dummy_tweets.csv"))
df['date'] = pd.date_range(start='2025-01-01', periods=len(df), freq='D')  # Simulated dates

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    policies = df['policy'].unique().tolist()
    selected_policy = request.form.get('policy', policies[0]) if request.method == 'POST' else policies[0]
    search_query = request.form.get('search', '').lower()
    sentiment_filter = request.form.get('sentiment', 'all')
    date_start = request.form.get('date_start', df['date'].min().strftime('%Y-%m-%d'))
    date_end = request.form.get('date_end', df['date'].max().strftime('%Y-%m-%d'))

    # Filter data
    filtered_df = df[df['policy'] == selected_policy]
    if search_query:
        filtered_df = filtered_df[filtered_df['text'].str.lower().str.contains(search_query, na=False)]
    if sentiment_filter != 'all':
        sentiment_map = {'negative': 0, 'neutral': 1, 'positive': 2}
        filtered_df = filtered_df[filtered_df['label'] == sentiment_map[sentiment_filter]]
    filtered_df = filtered_df[
        (filtered_df['date'] >= date_start) & (filtered_df['date'] <= date_end)
    ]

    # Debug prints
    print("Filtered DF size:", len(filtered_df))
    print("Filtered DF labels:", filtered_df['label'].value_counts().to_dict())
    
    # Sentiment trends
    sentiment_plot = plot_sentiment_trends(filtered_df)

    # Word cloud
    wordcloud_img = generate_wordcloud(filtered_df['cleaned_text'].tolist())

    # Themes
    themes = extract_themes(df, selected_policy)

    # Sentiment distribution
    sentiment_counts = filtered_df['label'].value_counts().reindex([0, 1, 2], fill_value=0).to_dict()
    sentiment_distribution = {
        'Negative': sentiment_counts.get(0, 0),
        'Neutral': sentiment_counts.get(1, 0),
        'Positive': sentiment_counts.get(2, 0)
    }
    print("Sentiment counts:", sentiment_counts)
    print("Sentiment distribution:", sentiment_distribution)

    # Summary metrics
    total_tweets = len(filtered_df)
    sentiment_percentages = {
        'Negative': (sentiment_distribution['Negative'] / total_tweets * 100) if total_tweets > 0 else 0,
        'Neutral': (sentiment_distribution['Neutral'] / total_tweets * 100) if total_tweets > 0 else 0,
        'Positive': (sentiment_distribution['Positive'] / total_tweets * 100) if total_tweets > 0 else 0
    }

    # ... (rest of the code unchanged) ...

    # Categorized tweets
    negative_tweets = filtered_df[filtered_df['label'] == 0][['text']].head(5).to_dict('records')
    neutral_tweets = filtered_df[filtered_df['label'] == 1][['text']].head(5).to_dict('records')
    positive_tweets = filtered_df[filtered_df['label'] == 2][['text']].head(5).to_dict('records')

    # Keywords for bar chart
    keywords_data = [{'keyword': k, 'count': c} for k, c in themes['keywords'][:10]]

    # Policy comparison data
    policy_comparison = []
    for policy in policies:
        policy_df = df[df['policy'] == policy]
        counts = policy_df['label'].value_counts().reindex([0, 1, 2], fill_value=0).to_dict()
        policy_comparison.append({
            'policy': policy,
            'negative': counts.get(0, 0),
            'neutral': counts.get(1, 0),
            'positive': counts.get(2, 0)
        })

    return render_template(
        'index.html',
        policies=policies,
        selected_policy=selected_policy,
        sentiment_plot=sentiment_plot,
        wordcloud_img=wordcloud_img,
        keywords=keywords_data,
        topics=themes['topics'],
        sentiment_distribution=sentiment_distribution,
        negative_tweets=negative_tweets,
        neutral_tweets=neutral_tweets,
        positive_tweets=positive_tweets,
        total_tweets=total_tweets,
        sentiment_percentages=sentiment_percentages,
        search_query=search_query,
        sentiment_filter=sentiment_filter,
        date_start=date_start,
        date_end=date_end,
        policy_comparison=policy_comparison,
        min_date=df['date'].min().strftime('%Y-%m-%d'),
        max_date=df['date'].max().strftime('%Y-%m-%d')
    )

@app.route('/download_tweets', methods=['POST'])
def download_tweets():
    selected_policy = request.form.get('policy')
    search_query = request.form.get('search', '').lower()
    sentiment_filter = request.form.get('sentiment', 'all')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')

    # Filter data
    filtered_df = df[df['policy'] == selected_policy]
    if search_query:
        filtered_df = filtered_df[filtered_df['text'].str.lower().str.contains(search_query, na=False)]
    if sentiment_filter != 'all':
        sentiment_map = {'negative': 0, 'neutral': 1, 'positive': 2}
        filtered_df = filtered_df[filtered_df['label'] == sentiment_map[sentiment_filter]]
    filtered_df = filtered_df[
        (filtered_df['date'] >= date_start) & (filtered_df['date'] <= date_end)
    ]

    # Convert to CSV
    csv_buffer = io.StringIO()
    filtered_df[['text', 'label', 'policy', 'cleaned_text']].to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'{selected_policy}_tweets.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)