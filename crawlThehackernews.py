import requests
from bs4 import BeautifulSoup
import re
import json

baseURL = "https://thehackernews.com/search/label/Vulnerability"

def GetPageContent(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

def GetURLs(soup):
    articles = soup.find_all('a')
    urls = []
    for x in range(0,len(articles)):
        url = articles[x].get('href')
        url_regex = re.compile(r'(https?://thehackernews.com/2023/\S+)')
        url_match = url_regex.search(url)
        if url_match:
            urls.append(url)
    return urls

def ParseContent(content):
    pattern = re.compile(r'<p>(.*?)</p>')
    matches = pattern.findall(content)
    pattern2 = re.compile(r'<a.*?>(.*?)</a>')
    for i, match in enumerate(matches):
        matches[i] = re.sub(pattern2, '', match)
    return matches

def JsonFormat(Title, Date, Author, Content):
    title = Title
    date = Date
    author = Author
    content = Content
    article = {
        "title" : title,
        "date" : date,
        "author" : author,
        "content" : content
    }
    return article


def CrawlDataThreat(url):
    strings=[]
    soup=GetPageContent(url)
    for url in GetURLs(soup):
        soup = GetPageContent(url)
        title = soup.find("h1",class_="story-title")
        details =  soup.find_all("span",class_="author")
        contents = soup.find_all("p")
        textTitle = title.text
        textDate = details[0].text
        textAuthor = details[1].text
        with open("crawldata2.txt","a",encoding='utf-8') as file:
            file.write("Title: {} | Date: {} | Author: {}\n".format(title.text,details[0].text,details[1].text))
            for content in ParseContent(str(contents)):
                file.write(content + "\n")
                strings += content
            file.write("=================================*.*=================================\n")
        # with open("filejsonformat.json","a") as file:
        #     json.dump(JsonFormat(textTitle,textDate,textAuthor,strings),file)
        #     file.write("=================================*.*=================================\n")
            
CrawlDataThreat(baseURL)
