from django.shortcuts import render
from django.http import HttpResponse
import requests
from lxml import etree
from .models import BBCListSerializer, CNNListSerializer, HackerNewsListSerializer, NYTListSerializer, TechMemeListSerializer, ReuterListSerializer, TechCrunchListSerializer, MITListSerializer, WiredListSerializer, IEEEListSerializer
from rest_framework.renderers import JSONRenderer
# Create your views here.



l = ["description", "title", "link"]

def getXMLContent(URL):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return requests.get(URL, headers).content


def cnnRSSEngine(request):
    xml:str = requests.get("http://rss.cnn.com/rss/edition.rss").content
    js = getDataFromXML(xml,CNNListSerializer, {"title":"title", "description":"description", "link":"link", "pubDate":"pubDate", "guid":"guid", "{*}content":"image"})
    return HttpResponse(js)

def getHackerNewsEngine(request):
    xml:str = getXMLContent("https://hnrss.org/frontpage")
    js = getDataFromXML(xml, HackerNewsListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate","guid":"guid","comments":"comments" })
    return HttpResponse(js)

def getNYTEngine(request):
    xml:str = getXMLContent("https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
    js = getDataFromXML(xml, NYTListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid", "{*}content":"image","creator":"creator"})
    return HttpResponse(js)


def getTechMemeEngine(request):
    xml:str = getXMLContent("https://www.techmeme.com/feed.xml")
    js = getDataFromXML(xml, TechMemeListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid"})
    return HttpResponse(js)


def getReutersEngine(request):
    xml:str = getXMLContent("https://www.reutersagency.com/feed/?taxonomy=best-regions&post_type=best")
    js = getDataFromXML(xml, ReuterListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid"})
    return HttpResponse(js)



def getTechCrunchEngine(request):
    xml:str = getXMLContent("https://techcrunch.com/feed/")
    js = getDataFromXML(xml, TechCrunchListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid"})
    return HttpResponse(js)


def getMITEngine(request):
    xml:str = getXMLContent("https://news.mit.edu/rss/feed")
    print(xml)
    js = getDataFromXML(xml, MITListSerializer, {"title":"title", "description":"description", "link":"link","{*}encoded":"content", "pubDate":"pubDate"})
    return HttpResponse(js)


def getWiredEngine(request):
    xml:str = getXMLContent("https://www.wired.com/feed/rss")
    
    js = getDataFromXML(xml, WiredListSerializer, {"title":"title", "description":"description", "link":"link","{*}creator":"creator", "{*}thumbnail":"image", "guid":"guid", "pubDate":"pubDate"})
    return HttpResponse(js)

def getIeeeEngine(request):
    xml:str = getXMLContent("https://ieeetv.ieee.org/channel_rss/channel_57/rss")
    js = getDataFromXML(xml, IEEEListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid","{*}creator":"creator"})
    return HttpResponse(js)


def getHowToGeekEngine(request):
    xml:str = getXMLContent("https://feeds.howtogeek.com/howtogeek")
    js = getDataFromXML(xml, BBCListSerializer, {"title":"title","description":"description","link":"link",
        "pubDate":"pubDate", "guid":"guid", "{*}creator":"creator", "{*}encoded":"description"})
    return HttpResponse(js)


def getARSTechnicaEngine(request):
    xml:str = getXMLContent("https://feeds.arstechnica.com/arstechnica/index")
    return HttpResponse(xml)


def getBBCEngine(request):
    xml:str = getXMLContent("https://feeds.bbci.co.uk/news/technology/rss.xml")
    print(xml)
    js = getDataFromXML(xml, BBCListSerializer, {"title":"title", "description":"description", "link":"link","pubDate":"pubDate", "guid":"guid"})
    print(js)
    return HttpResponse(js)


def getDataFromXML(xml, ListSerializer ,tagDict):
    root = etree.fromstring(xml)

    items = []
    tags = tagDict.keys()


    channel = root.find("channel")


    headerTitle = channel.find("title").text
    headerDescr = channel.find("description").text
    headerLink = channel.find("link").text
    headerImage = channel.find("image")
    if headerImage:
        headerImage = headerImage.find("url").text


    header = {
        "title":headerTitle,
        "description":headerDescr,
        "link":headerLink,
        "image":headerImage
        }


    for item in root.iter("item"):
        newItem = {}
        for tag in tags:
            child = item.find(".//"+tag)
            if tagDict[tag] == "image" and child is not None: # handle media content seperately as url is inside attribute instead of text
                newItem[tagDict[tag]] = child.get("url")
            else:
                newItem[tagDict[tag]] = "" if child is None else child.text
        items.append(newItem)
    newsItems = ListSerializer(items, many=True)
    obj = {"header":header,"newsItems":newsItems.data}
    return JSONRenderer().render(obj)
