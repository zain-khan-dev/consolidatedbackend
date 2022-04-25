from email.policy import default
from operator import attrgetter, itemgetter
import xml.etree.ElementTree as ET
import requests
from collections import defaultdict

from rssfeeder.utils.Constants import MAPPED_ENDPOINTS

# If the element is not none returns the text otherwise returns none
def getText(item):
    if(item != None):
        text_value = item.text
        if(text_value is not None):
            return text_value[:2000]
        else:
            return None
    return item

# Builds the header received from the channel. This is the header for the whole page
def buildHeader(rssDict):

    tags = ["title", "link", "description", "category", "image"]

    tagsGetter = itemgetter(*tags)
    ele_list = [getText(tag) for tag in tagsGetter(rssDict)]
    
    result_dict = {k:v for k,v in zip(tags, ele_list)}
    return result_dict




def getMappedURL(channel):
    return MAPPED_ENDPOINTS[channel]



def get_rss_from_url(url):
    return getRSSData(url)



def getMultipleRssData(rssChannels):
    resultantDict = {"header":None, "items":[]}
    for channel in rssChannels:
        channelDict = getRSSData(getMappedURL(channel))
        resultantDict["items"].extend(channelDict["items"])
    print(resultantDict)
    return resultantDict
    


# Receives item as paramter and returns an item node for the api
def buildItemNodes(item):
    # taking none value for the categories that are not present
    tags = ["link", "title", "description", "category", "pubDate", "comments"]
    # build a dict with tag as the 
    eleDict = defaultdict(lambda:None, {ele.tag:ele for ele in item})
    eleGetter = itemgetter(*tags)
    result_item_list = [getText(tag) for tag in eleGetter(eleDict)]
    result_item_dict = {k:v for k, v in zip(tags, result_item_list)}
    return result_item_dict


# To parse the data correctly we need to assume the schema for the rss we are feeding int
# Assuming the following structure for tags
# rss
# |- channel
# | - - title
# | - - link
# | - - description
# | - - doc
# | - - generator
# | - - lastBuildDate
# | - - atom links
# | - - items list
# assuming items list is contained in channel node
# we get the list for items
def parseXMLData(data):
    rss = ET.fromstring(data) # returned is the rss node
    channel  =rss.find("channel") # get the channel node
    rssDict = defaultdict(lambda:None, {ele.tag:ele for ele in channel if ele.tag != "item"})
    print(rssDict)
    header = buildHeader(rssDict)
    # print(header_metadata)
    # filter for all the items element there are in the channel
    items = [ele for ele in channel[3:] if ele.tag == "item"] 
    itemNodes = [buildItemNodes(item) for item in items]
    return {
        "header": header,
        "items": itemNodes
    }

def getRSSData(siteURL):
    request = requests.get(siteURL)
    if(request.status_code >=200 and request.status_code < 300):
        rssDict = parseXMLData(request.content)
        print(rssDict)
        return rssDict
    else:
        print("Could not query")
        return {"error":"There was a problem parsing the xml data"}
