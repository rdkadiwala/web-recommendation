import re
import urllib2
import html2text
import socket
# from preprocess_data import filter_content
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
# from langdetect import detect


class MyHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def __init__(self):
        HTMLParser.__init__(self)
        self.description = None
        self.keyword = None

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            for attr in attrs:
                if (attr[0] == 'name') or (attr[0] == 'Name'):
                    descs = re.search(r'description', attr[1], re.M | re.I)
                    descc = re.search(r'Description', attr[1], re.M | re.I)
                    keys = re.search(r'keywords', attr[1], re.M | re.I)
                    keyc = re.search(r'Keywords', attr[1], re.M | re.I)
                    if descs:
                        if descs.group() == 'description':
                            self.description = attr[1]
                    if descc:
                        if descc.group() == 'Description':
                            self.description = attr[1]
                    if keys:
                        if keys.group() == 'keywords':
                            self.keyword = attr[1]
                    if keyc:
                        if keyc.group() == 'Keywords':
                            self.keyword = attr[1]


def data_request(url):
    # url = 'https://www.onlinesbi.com/'
    user_agent = 'Mozilla/5.0 (Windows NT 8.1; Win32; x86)'
    # user_agent = 'Googlebot/2.1 (+http://www.google.com/bot.html)'
    accept_lang = 'en-US,en;q=0.8'
    header = {'User-Agent': user_agent, 'accept-language': accept_lang}
    req = urllib2.Request(url, None, header)
    try:
        page = urllib2.urlopen(req, timeout=15)
    except urllib2.HTTPError:
        return None
    except urllib2.URLError:
        return None
    except socket.timeout:
        return None
    except Exception:
        return None

    if (str(page.getcode()) == str(200)) and (page.geturl() == url):

        last_modified_date = page.info().getheader('Last-Modified')
        if last_modified_date is None:
            last_modified_date = page.info().getheader('date')
        elif last_modified_date is None:
            last_modified_date = page.info().getheader('Date')

        page = page.read().decode('utf-8', 'ignore')
        parser = MyHTMLParser()
        parser.feed(page)
        soup = BeautifulSoup(page, 'html.parser')

        htmltotext = html2text.HTML2Text()
        htmltotext.ignore_links = True
        htmltotext.ignore_images = True
        text = htmltotext.handle(page)
        # try:
        #     content_lang = detect(text)
        # except Exception, e:
        #     return 'Lang detection Error'
        #
        # if content_lang == "en":

        links = set()
        for link in soup.findAll('a'):
            link = link.get('href')
            if link is None:
                continue
            elif link.startswith('//'):
                links.add('https:' + link)
            elif link.startswith('https'):
                links.add(link)
            elif link.startswith('http'):
                links.add(link)
            elif link.startswith('/'):
                if url.endswith('/'):
                    links.add(url[:-1] + link)
                else:
                    links.add(url + link)
        with open('/home/jarvisr/Datasets/temp_list.txt', 'a') as fin:
            fin.seek(0,2)
            for link in links:
                fin.write(link + '\n')

        Description = ''
        Keywords = ''

        if parser.description is not None:
            Description = soup.find("meta", {"name": parser.description})['content']
        if parser.keyword is not None:
            Keywords = soup.find("meta", {"name": parser.keyword})['content']

        regx = re.compile("[^a-zA-Z ]")
        text = regx.sub('', text).lower()
        description = regx.sub('', Description).lower()
        keywords = regx.sub('', Keywords).lower()
        title = regx.sub('',soup.title.string).lower()
        content = text
        Url = url
        # print 'URL : ' + Url
        # print 'Title : ' + Title
        # print 'Description : ' + Description
        # print 'Keyword : ' + Keywords
        # print 'Content : ' + Content
        # print 'Date : ' + str(last_modified_date)
        # from datetime import datetime
        # print 'Sys Time : ' + str(datetime.now())

        sql = "INSERT INTO `internet_data` (`url`, `title`,`description`, `keywords`,  `content`, `last_modified`) " \
              "VALUES ('" + Url.encode('UTF-8', 'ignore') + "','" + title + "', '" + description + "','" \
              + keywords + "','" + content + "','" + str(last_modified_date).encode('UTF-8', 'ignore') + "')"
        with open('/home/jarvisr/Datasets/code-200.txt', 'a') as successful:
            successful.write(Url + '\n')
        return sql
        # else:
        #     return 'Lang other then english'

    else:
        with open('/home/jarvisr/Datasets/other_code-200.txt', 'a') as unsuccessful, open('/home/jarvisr/Datasets/temp_list.txt', 'a') as redirect:
            unsuccessful.write(url + '\n')
            redirect.write(page.geturl() + '\n')
        return 'Redirect or 200 error'

# print data_request('https://l.facebook.com/l.php?u=https%3A%2F%2Finstagram.com%2F&h=ATPBi1rVbzVT0PvWZIrz-Ppa7vKMsAIUWBjDjLM4zir9kgRgNlCfPt5xH8iipKBamWXOFqdQOtViqxLbuVUTMEFOLFNEJ7OQXFRBRoVxFxrJpjNxwPXhsE4&s=1')
# print data_request('https://app.appsflyer.com/id305343404?pid=tumblr_internal&c=signup_page')
# print data_request('https://www.facebook.com/')
# print data_request('https://stackoverflow.com')
# print data_request('https://en.wikipedia.org/wiki/Main_Page')
# print data_request('https://www.google.co.in/')
# print data_request('https://www.rbi.org.in/')