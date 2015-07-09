"""
Get Video links, title and date of video posted
"""

import requests
import logging
from bs4 import BeautifulSoup

LOGGING = logging.getLogger(__name__)


class YoutubeScrape(object):
    """ youtube scrape class """

    youtube = "https://www.youtube.com"
    video_divs = []
    video_infos = []

    def __init__(self, user):
        self.url = self.youtube + "/user/" + user + "/videos/"
        self.html = requests.get(self.url).content.strip()
        self.soup = BeautifulSoup(self.html)
        self.process_data()

    def get_video_divs(self):
        """ get all the video div tags from soup """
        self.video_divs = self.soup.findAll(
            "li", {"class": "channels-content-item"})[:15]

    def process_data(self):
        """ get all video infos in json from list of single video soups """
        if not self.video_divs:
            self.get_video_divs()
        for video_soup in self.video_divs:
            video_info = self.get_video_info(video_soup)
            if video_info:
                self.video_infos.append(video_info)

    def get_video_info(self, single_video_soup):
        """ get video title and url from single video soup """
        video_header = single_video_soup.find("h3",
                                              {"class": "yt-lockup-title"})
        if not video_header:
            return {}
        video_tag = video_header.find("a")
        video_attrs = video_tag.attrs
        if not video_attrs.get("href"):
            return {}
        watch_url = video_attrs.get("href", "")
        if watch_url.startswith("/playlist"):
            return {}
        video_url = self.youtube + video_attrs.get("href", "")
        title = video_attrs.get("title", "")
        LOGGING.debug("Getting info of video " + video_url)
        video_html = requests.get(video_url).content.strip()
        video_soup = BeautifulSoup(video_html)
        published_text = video_soup.find("strong",
                                         {"class": "watch-time-text"}).text
        published_text = published_text.replace("Published on ", "")
        return {"url": video_url,
                "title": title,
                "created": published_text}

    # def get_time_of_video(self, single_video_soup):
    #    time_diff = single_video_soup.find("ul",
    #                                       {"class": "yt-lockup-meta-info"}).\
    #        findAll("li")[-1].text
    #    time_diffs = [t.strip() for t in time_diff.split()]
    #    time_diff_int = int(time_diffs[0])
    #    day_diff, week_diff, month_diff = 0
    #    if "day" in time_diffs[1]:
    #        multiplier = 1
    #    if "month"
