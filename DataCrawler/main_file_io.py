from itertools import islice
from multiprocessing.pool import ThreadPool
from time import time as timer

import pymysql.cursors
from pymysql import MySQLError

import Crawler

error_list = ['Redirect or 200 error', 'Lang other then english', 'Lang detection Error']

def fetch_url(url):
    # print "-> %r requesting" % (url)
    url = url.rstrip('\n')
    try:
        response = Crawler.data_request(url)
        # print "-> %r request complete" % (url)
        if (response is not None) and (response not in error_list):
            return url, response, None
        else:
            return url, None, response
    except Exception as e:
        return url, None, e

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='', db='project_db',
                           charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    a = conn.cursor()
    count = 2
    while count > 0:
        urls = []
        with open('/home/jarvisr/Datasets/url_list.txt', 'r') as url_read:
            while True:
                urls = list(islice(url_read, 20))

                start = timer()
                results = ThreadPool(10).imap(fetch_url, urls)
                with open('/home/jarvisr/Datasets/log.txt', 'a') as logfile:
                    for url, sql, error in results:
                        if (error is None) and (sql not in error_list) and (sql is not None):
                            logfile.write("-> %r fetched in %ss\n" % (url, timer() - start))
                            try:
                                a.execute(sql)
                            except MySQLError as e:
                                print('Got error {!r}, errno is {}'.format(e, e.args[0]))
                            conn.commit()
                            print "-> %r fetched in %ss" % (url, timer() - start)
                        else:
                            print "-> error fetching %r: %s" % (url, error)
                            logfile.write("-> error fetching %r: %s\n" % (url, error))

                if len(urls) < 20:
                    break
        # with open('url_collection.txt', 'a') as collection:
        #     fin = open('url_list.txt', 'r')
        #     for line in fin.readline():
        #         collection.write(line)
        #     fin.close()

        with open('/home/jarvisr/Datasets/url_list.txt', 'w') as active_list:
            fin = open('/home/jarvisr/Datasets/temp_list.txt', 'r')
            for line in fin.readlines():
                active_list.write(line)
            fin.close()

        open('/home/jarvisr/Datasets/temp_list.txt', 'w').close()
        count -= 1
    conn.close()

    # print("Elapsed Time: %s" % (timer() - start,))
    # sql data insert
    # conn = pymysql.connect(host='localhost', user='root', password='dbpass@', db='project_db',
    #                            cursorclass=pymysql.cursors.DictCursor)
    # a = conn.cursor()
    # a.execute(sql)
    # conn.commit()
    # conn.close()