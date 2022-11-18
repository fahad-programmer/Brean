import random
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import WebPages
from django.views.generic import ListView
import logging
from textblob import TextBlob

# Logging basic file configuration
logging.basicConfig(filename='app.log', filemode='a',
                    format="%(process)d-%(levelname)s-%(message)s")


class Viper(ListView):

    current_url = "https://www.bbc.com"
    waiting_urls = []
    crawled_urls = []

    def __init__(self) -> None:
        self.engine()

    def parser(self) -> None:
        global soup
        page = requests.get(self.current_url)
        soup = BeautifulSoup(page.content, "lxml")

        # Now getting the desired thing from the page
        try:
            global title, meta_description, keyword
            title = soup.find("meta", property="og:title")
            meta_description = soup.find("meta", attrs={'name': 'description'})
            keyword = soup.find("meta", attrs={'name': 'keywords'})

            title = title["content"]
            meta_description = meta_description["content"]
            keyword = keyword["content"]

        except Exception as e:
            logging.error(
                f"Error in finding the data on the web page {self.current_url}")

    def add_to_database(self) -> None:
        try:
            if keyword != '' or keyword != None:
                key_list = keyword
            else:
                key_list = TextBlob(meta_description).noun_phrases
                ', '.join(keylist)
                print(key_list)
            main_obj = WebPages(
                title=title, meta_description=meta_description, keywords=key_list, url=self.current_url)
            main_obj.save()
        except Exception as e:
            logging.error(
                "Error occured while putting the values in the database")
            pass

    def getting_links(self) -> None:
        try:
            for link in soup.findAll('a'):
                crawled_url = link.get('href')
                if crawled_url:
                    if '?' in crawled_url:
                        crawled_url = crawled_url.split("?")[0]
                    if crawled_url not in self.waiting_urls and crawled_url != self.current_url and crawled_url not in self.crawled_urls:
                        if 'http' in crawled_url:
                            self.waiting_urls.append(crawled_url)
                        elif ':javascript' in crawled_url or "#" == crawled_url:
                            pass
                        else:
                            self.waiting_urls.append(
                                f"{self.current_url}{crawled_url}")
        except Exception as e:
            pass

    def queue_manager(self) -> None:
        # Adding crawled url into the cralwed list
        self.crawled_urls.append(self.current_url)
        # changing the current url
        self.current_url = self.waiting_urls[random.choice(range(0, 5))]
        # removing the element from the list
        self.waiting_urls.remove(self.current_url)

    def engine(self) -> None:
        # The main engine method that will start the crawler
        while True:
            self.parser()
            self.add_to_database()
            self.getting_links()
            self.queue_manager()

    def __repr__(self) -> str:
        return f"The title is {title} with meta description is {meta_description} \n with the {keyword}"


# Create your views here.
