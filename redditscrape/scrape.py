import praw
from datetime import datetime

class RedditScrape(object):
    """ Reddit Scraping object using praw """

    def __init__(self, sub_reddit, num=15):
        self.sub_reddit = sub_reddit
        self.num_of_articles = num
        self.articles_info = []
        self.multimedia = False
        self.topics = []

    def set_multimedia(self):
        """ sets the multimedia boolean to true """
        self.multimedia = True

    def get_subreddit(self):
        reddit_obj = praw.Reddit(user_agent='app')
        self.subreddit = reddit_obj.get_subreddit(self.sub_reddit)

    def _articles(self):
        if not self.topics:
            self.get_subreddit()
        self.topics = self.subreddit.get_hot(limit=self.num_of_articles)

    def get_article_information(self):
        if not self.multimedia:
            return ()
        self._articles()
        article_objs = [i for i in self.topics]
        for article in article_objs:
            single_article = {}
            media_obj = article.media.get('oembed')
            single_article['url'] = media_obj.get('url')
            single_article['title'] = article.title
            created = datetime.fromtimestamp(article.created)
            single_article['created'] = created.isoformat()
            self.articles_info.append(single_article)
        return self.articles_info

    @property
    def articles(self):
        return self.get_article_information()
