import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalyzer:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def get_tweets(self, keyword, count=100):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=keyword, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if hasattr(tweet, 'retweeted_status'):
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.retweeted_status.full_text)
                tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def clean_tweet(self, tweet):
        cleaned_tweet = tweet.lower()
        cleaned_tweet = re.sub(r'@[A-Za-z0-9]+', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'#', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'RT[\s]+', '', cleaned_tweet)
        cleaned_tweet = re.sub(r'https?:\/\/\S+', '', cleaned_tweet)
        return cleaned_tweet

    def plot_sentiment_distribution(self, tweets):
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        for tweet in tweets:
            sentiment_counts[tweet['sentiment']] += 1

        labels = sentiment_counts.keys()
        sizes = sentiment_counts.values()
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        plt.show()

    def run_sentiment_analysis(self, keyword):
        tweets = self.get_tweets(keyword)
        self.plot_sentiment_distribution(tweets)

if __name__ == "__main__":
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    access_token = 'your_access_token'
    access_token_secret = 'your_token_secret'

    analyzer = SentimentAnalyzer(consumer_key, consumer_secret, access_token, access_token_secret)
    analyzer.run_sentiment_analysis("#examplehashtag")
