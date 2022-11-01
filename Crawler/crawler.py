from bs4 import BeautifulSoup
import requests
from .models import WebPages
import logging

#Logging basic file configuration
logging.basicConfig(filename='app.log', filemode='a', format="%(process)d-%(levelname)s-%(message)s")

class Viper:

    current_url = "https://docs.djangoproject.com/en/4.1/"
    waiting_urls = []

    def __init__(self) -> None:
        self.engine()

    def parser(self) -> None:
        global soup
        page = requests.get(self.current_url)
        soup = BeautifulSoup(page.content, "lxml")

        #Now getting the desired thing from the page
        try:
            global title, meta_description, keyword
            title = soup.find("meta", property="og:title")
            meta_description = soup.find("meta", attrs={'name':'description'})
            keyword = soup.find("meta", attrs={'name':'keywords'})

        except Exception as e:
            logging.error(f"Error in finding the data on the web page {self.current_url}")

    def add_to_database(self) -> None:
        try:
            WebPages(title=title, meta_description=meta_description, keywords=keyword, url=self.current_url)
            WebPages.save()
        except Exception as e:
            logging.error("Error occured while putting the values in the database")
            pass

    def getting_links(self) -> None:
        for link in soup.findAll('a'):
            if 'https' in link.get('href'):
                self.waiting_urls.append(link.get('href'))
            else:
                self.waiting_urls.append(f"{self.current_url}{link.get('href')}")
        print(self.waiting_urls)

    def queue_manager(self) -> None:
        #changing the current url
        self.current_url = self.waiting_urls[0]
        #removing the element from the list
        self.waiting_urls.remove(self.current_url)

    def engine(self) -> None:
        #The main engine method that will start the crawler
        while True:
            self.parser()
            self.add_to_database()
            self.getting_links()
            self.queue_manager()


    def __repr__(self) -> str:
        return f"The title is {title} with meta description is {meta_description} \n with the {keyword}"






