# Libraries
# from itertools import islice
# from multiprocessing.pool import ThreadPool
from time import time as timer

# Project File
import preprocess_data


if __name__ == '__main__':

    # count = 0
    with open('/home/jarvisr/Datasets/internet_data.csv', 'r') as internet_data, open('/home/jarvisr/Datasets/processed_data.csv', 'a') as processed_data, open('/home/jarvisr/Datasets/preprocessing_log.txt', 'a') as log:
        for line in internet_data:
            temp = line.split(',')
            row_id = temp[0].strip('"')
            content = temp[5].strip('"')
            start = timer()
            print row_id
            after_cleaning = preprocess_data.filter_content(content)
            log.write("-> id - %r , input-len = %r , output-len = %r , processed in %ss\n" % (row_id, len(content), len(after_cleaning), timer() - start))
            processed_data.write(row_id+','+after_cleaning+'\n')
            # count += 1
            # if count > 5:
            #     break
    print 'Data processing task complete'
        # while True:
        #     lines = list(islice(internet_data, 11))
        #     noisy_data = []
        #     for line in lines:
        #         temp = line.split(',')
        #         noisy_data.append(temp[0]+','+temp[5])
        #
        #     start = timer()
        #     result = ThreadPool(5).imap_unordered(preprocess_data.filter_content, noisy_data)
        #     with open('processed_data.csv', 'a') as processed_data, open('preprocessing_log.txt', 'a') as log:
        #         for line in result:
        #             temp = line.split(',')
        #             a1 = temp[0]
        #             a2 = temp[1]
        #             log.write("-> id - %r , len - %r , processed in %ss\n" % (a1, len(a2), timer()-start))
        #             processed_data.write(line+'\n')
        #
        #     if len(lines) < 10:
        #         break
