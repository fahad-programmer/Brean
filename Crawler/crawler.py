from bs4 import BeautifulSoup
import requests
import logging
from textblob import TextBlob

'''
You May need to run following to lines in python terminal if program desn;t run properly
>> import nltk
>> nltk.download('brown')
>> nltk.download('punkt')

* Remove this comment after running the commands
'''

# Logging basic file configuration
logging.basicConfig(filename='app.log', filemode='a',
                    format="%(process)d-%(levelname)s-%(message)s")


class Viper:

    current_url = "https://www.yahoo.com/"
    waiting_urls = []
    crawled_urls = []
    sites = {}

    def __init__(self) -> None:
        self.engine()

    def parser(self) -> None:
        global soup
        page = requests.get(self.current_url)
        soup = BeautifulSoup(page.content, "lxml")

        # Now getting the desired thing from the page
        try:
            global title, meta_description, keyword
            title = soup.find("title").string
            meta_description = soup.find(
                "meta", attrs={'name': 'description'})["content"]
            keyword = soup.find("meta", attrs={'name': 'keywords'})["content"]
        except Exception as e:
            logging.error(
                f"Error in finding the data on the web page {self.current_url}")

    def add_to_database(self) -> None:
        try:
            # WebPages(title=title, meta_description=meta_description, keywords=keyword, url=self.current_url)
            # WebPages.save()
            if keyword != '':
                key_list = keyword.split(", ")
            else:
                key_list = TextBlob(meta_description).noun_phrases
            self.sites[self.current_url] = [self.current_url, title,
                                            meta_description, key_list]
            print(self.sites[self.current_url])
        except Exception as e:
            logging.error(
                "Error occured while putting the values in the database")
            pass

    def getting_links(self) -> None:
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
            else:
                continue
        # print(self.waiting_urls)
        # exit()

    def queue_manager(self) -> None:
        # Adding crawled url into the cralwed list
        self.crawled_urls.append(self.current_url)
        # changing the current url
        self.current_url = self.waiting_urls[0]
        # removing the element from the list
        self.waiting_urls.remove(self.current_url)

    def engine(self) -> None:
        # The main engine method that will start the crawler

        while True:
            # Scrapping current url web information
            self.parser()
            # Title Check
            if not title:
                continue
            # Add Scraped Data into the database
            self.add_to_database()
            # Get Forward links
            self.getting_links()
            # Set the next url to scrape
            self.queue_manager()

    def __repr__(self) -> str:
        return f"The title is {title} with meta description is {meta_description} \n with the {keyword}"


Viper()
