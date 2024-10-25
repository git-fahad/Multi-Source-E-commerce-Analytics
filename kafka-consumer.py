import psycopg2
from kafka import KafkaConsumer
import json
from textblob import TextBlob

# For this project I am using Postgres db installed on my machine
conn = psycopg2.connect(
    host="localhost",
    database="sentiment_analysis",
    user="postgres",
    password="newpass123"
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    'social-sentiment-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='tweet-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

for message in consumer:
    tweet = message.value
    tweet_id = tweet['id_str']
    tweet_text = tweet['text']
    tweet_created_at = tweet['created_at']
    sentiment = analyze_sentiment(tweet_text)

    cursor.execute("""
        INSERT INTO tweets (tweet_id, tweet_text, tweet_created_at, sentiment)
        VALUES (%s, %s, %s, %s)
    """, (tweet_id, tweet_text, tweet_created_at, sentiment))

    conn.commit()
    print(f"Stored tweet: {tweet_text} with sentiment: {sentiment}")

cursor.close()
conn.close()
