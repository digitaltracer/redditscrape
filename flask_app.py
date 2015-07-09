"""
Simple flask app to get articles
"""

from flask import Flask, Response
import json
import sys
import os
from redditscrape.scrape import RedditScrape
from youtubescrape.scrape import YoutubeScrape


PACKAGE_PATH = os.path.dirname(__file__)
if PACKAGE_PATH not in sys.path:
    sys.path.append(PACKAGE_PATH)


APP = Flask("redditscrape")


@APP.route("/reddit/<subreddit>", defaults={'count': 15}, methods=['GET'])
@APP.route("/reddit/<subreddit>/<count>", methods=['GET'])
def get_result(subreddit, count):
    """ get the latest articles and send it as json """
    rs_object = RedditScrape(subreddit, count)
    rs_object.set_multimedia()
    result = rs_object.articles
    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")


@APP.route("/youtube/<channel>", defaults={"count": 10}, methods=["GET"])
@APP.route("/youtube/<channel>/<count>", methods=["GET"])
def get_youtube_urls(channel, count):
    """ fetches youtube video infos and returns as json """
    ys_object = YoutubeScrape(channel)
    video_urls = ys_object.video_infos[:count]
    return Response(response=json.dumps(video_urls),
                    status=200,
                    mimetype="application/json")

if __name__ == "__main__":
    APP.run(host='0.0.0.0', debug=True)
