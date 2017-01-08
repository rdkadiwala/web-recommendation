# coding=UTF-8
def decode_verbose(bs, index):
    try:
        result = bs.decode('utf-8', 'strict')
    except UnicodeDecodeError:
        result = bs.decode('utf-8', 'ignore')
        print "Problematic byte string at index {2}: {0} | Ignored: {1}".format(bs, result, index)
    return result


def tdf(content, message):
    import pandas as pd
    import nltk

    content = nltk.regexp_tokenize(content, r'\S+')
    content = [ch for ch in content]
    fdist = nltk.FreqDist(content)
    count_frame = pd.DataFrame(fdist.items(), columns=['Word', 'Count'])
    count_frame = count_frame.sort_values('Count', ascending=False)
    print message+str(len(count_frame))
    return count_frame.set_index('Word', drop=False)


def wf_bar(wf, message):
    import matplotlib.pyplot as plt

    plt.style.use('ggplot')
    fig = plt.figure(figsize=(12, 7))
    ax = fig.gca()
    wf['Count'][:60].plot(kind='bar', ax=ax)
    ax.set_title('Frequency of most common words ('+message+')')
    ax.set_ylabel('Frequency of word')
    ax.set_xlabel('Word')
    plt.show()

    return 'Done'


def plot_cwf(wf):
    import matplotlib.pyplot as plt

    plt.style.use('ggplot')
    word_count = float(wf['Count'].sum(axis=0))
    wf['Cum'] = wf['Count'].cumsum(axis=0)
    wf['Cum'] = wf['Cum'].divide(word_count)
    fig = plt.figure(figsize=(12, 7))
    ax = fig.gca()
    wf['Cum'][:60].plot(kind='bar', ax=ax)
    ax.set_title('Cumulative fraction of total words vs words')
    ax.set_ylabel('Cumulative fraction')
    ax.set_xlabel('Word')
    plt.show()

    return 'Done'


def filter_content(content):
    import data_segmentation
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords

    content = data_segmentation.word_segment(content)
    # print 'Word Segmentation : '+content
    # twf = tdf(content, 'After Segmentation -> ')
    # wf_bar(twf, 'After Segmentation')

    temp = content.split()
    stop_words = stopwords.words('english')
    content = ' '.join([word for word in temp if (word not in set(stop_words) and len(word) > 1)])
    # print 'Stop Word Removal : '+content
    # twf = tdf(content, 'After Stop word removing -> ')
    # wf_bar(twf, 'After Stop word removing')

    # temp = [decode_verbose(t, i) for i, t in enumerate(content.split())]
    lemtz = WordNetLemmatizer()
    temp = content.split()
    temp = [lemtz.lemmatize(word) for word in temp]
    content = ' '.join(word for word in temp if len(word) > 1)
    # print 'Lemmatization : '+content
    # wf = tdf(content, 'After Lemmatization(nltk) -> ')
    # wf_bar(wf, 'After Lemmatization')
    return content
