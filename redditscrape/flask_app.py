"""
Simple flask app to get articles
"""

from flask import Flask, Response
import json
from redditscrape.scrape import RedditScrape


APP = Flask("redditscrape")


@APP.route("/<subreddit>", defaults={'count': 15}, methods=['GET'])
@APP.route("/<subreddit>/<count>", methods=['GET'])
def get_result(subreddit, count):
    """ get the latest articles and send it as json """
    rs_object = RedditScrape(subreddit, count)
    rs_object.set_multimedia()
    result = rs_object.articles
    return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")

if __name__ == "__main__":
    APP.run(host='0.0.0.0', debug=True)
