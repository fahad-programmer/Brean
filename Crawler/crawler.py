from bs4 import BeautifulSoup
import requests

# url = "https://www.facebook.com"
# page = requests.get(url)

# soup = BeautifulSoup(page.content, "lxml")

# title = soup.find("meta", property="og:title")
# url = soup.find("meta", property="og:description")


# print(title["content"])
# print(url["content"])

class Viper:


    def __init__(self, start_url) -> None:
        self.start_url = start_url
        self.parser()

    def parser(self):
        page = requests.get(self.start_url)
        soup = BeautifulSoup(page.content, "lxml")

        #Now getting the desired thing from the page
        try:
            global title, meta_description, keyword
            title = soup.find("meta", property="og:title")
            meta_description = soup.find("meta", attrs={'name':'description'})
            keyword = soup.find("meta", attrs={'name':'keywords'})
        except Exception as e:
            print(e)

    def __repr__(self) -> str:
        return f"The title is {title} with meta description is {meta_description} \n with the {keyword}"




main_obj = Viper("https://www.coinglass.com/FundingRate")
print(main_obj)


