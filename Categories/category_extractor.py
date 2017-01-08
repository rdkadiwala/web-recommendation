# coding=utf-8

with open('/home/jarvisr/Datasets/categories.txt','r') as inputfile, open('/home/jarvisr/Datasets/categories.txt','a') as outputfile:
    count = 0
    for line in inputfile:
        word = line.rstrip('\n').split('/')
        print word
        count += 1
        if count > 4:
            break