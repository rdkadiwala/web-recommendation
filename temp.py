# coding=utf-8

# import nltk
# nltk.download()


# https://www.google.co.in/
# https://stackoverflow.com/
# https://in.yahoo.com/
# https://www.facebook.com/
# https://www.youtube.com/
# https://www.quora.com/
# http://www.universetoday.com/
# http://timesofindia.indiatimes.com/
# https://www.flipkart.com/
# https://www.snapdeal.com/
# http://www.gametop.com/
# http://www.moneycontrol.com/
# https://en.wikipedia.org/wiki/Main_Page
# http://www.wikihow.com/Main-Page
# https://www.onlinesbi.com/
# https://www.rbi.org.in/

with open('/home/jarvisr/Datasets/processed_data.csv','r') as inputfile, open('/home/jarvisr/Datasets/data.txt','a') as outputfile:
    for line in inputfile:
        outputfile.write(line.split(',')[1])