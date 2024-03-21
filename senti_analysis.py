from flask import Flask, request, render_template
from textblob import TextBlob
from newsapi import NewsApiClient
import matplotlib.pyplot  as plt

import os

app = Flask(__name__,template_folder="templates")

# Initialize News API client with your API key
newsapi = NewsApiClient(api_key='e0ec64e92b45404985bc7d88a91d5601')

# Function to retrieve news articles related to the input stock
def retrieve_news(stock_symbol):
    # Retrieve top headlines related to the stock symbol
    articles = newsapi.get_everything(q=stock_symbol, language='en', sort_by='relevancy')

    # Extract article titles and descriptions
    news_articles = []
    for article in articles['articles']:
        title = article.get('title', '')
        description = article.get('description', '')
        news_articles.append(f"{title}. {description}")

    return news_articles


# Function to perform sentiment analysis on news articles
def perform_sentiment_analysis(news_articles):
    sentiment_scores = []
    for article in news_articles:
        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(article)
        sentiment_scores.append(analysis.sentiment.polarity)

    return sentiment_scores

# Function to aggregate sentiment scores
def aggregate_sentiment_scores(sentiment_scores):
    # Calculate average sentiment score
    avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
    print(avg_sentiment_score)

    return avg_sentiment_score

# Function to predict stock direction based on sentiment analysis
def predict_stock_direction(stock_symbol):
    # Step 1: Retrieve news articles
    news_articles = retrieve_news(stock_symbol)
    
    # Step 2: Perform sentiment analysis
    sentiment_scores = perform_sentiment_analysis(news_articles)
    
    # Step 3: Aggregate sentiment scores
    overall_sentiment = aggregate_sentiment_scores(sentiment_scores)
    
    # Step 4: Determine prediction based on overall sentiment
    if overall_sentiment > 0:
        return "The sentiment analysis indicates that the stock is likely to go up."
    elif overall_sentiment < 0:
        return "The sentiment analysis indicates that the stock is likely to go down."
    else:
        return "The sentiment analysis indicates that there is no clear direction for the stock."

@app.route('/')
def index():
    print(os.getcwd())
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    stock_symbol = request.form['stock_symbol']
    prediction = predict_stock_direction(stock_symbol)
    return render_template('result.html', stock_symbol=stock_symbol, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
