from itertools import count

import requests
import tweepy
from kafka import KafkaProducer
help(tweepy)

consumer_key = 'xxxxx'
consumer_secret = 'xxxxx'
access_token = 'xxxxx-xxxxx'
access_token_secret = 'xxxxx'

auth = tweepy.OAuth1UserHandler( consumer_key, consumer_secret,
                                 access_token, access_token_secret
)
api = tweepy.API(auth)

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_and_send_tweets(search_term, count, kafka_topic):
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=search_term, lang="en").items(count)

        for tweet in tweets:
            tweet_data = {
                "id": tweet.id_str,
                "text": tweet.text,
                "created_at": str(tweet.created_at),
                "user": tweet.user.screen_name
            }
            print(f"Sending tweet to Kafka: {tweet_data['text']}")

            # Send tweet to Kafka
            producer.send(kafka_topic, tweet_data)
            time.sleep(0.5)

    except Exception as e:
        print(f"Error fetching/sending tweets: {e}")

fetch_and_send_tweets('buying a new', 100, 'social-sentiment-topic')

# Close the Kafka producer after sending
producer.close()
