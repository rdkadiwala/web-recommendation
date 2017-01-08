# coding=utf-8
import gc
import wordsegment
# import sys
# sys.setrecursionlimit(10000)


def word_segment(text, limit=250):
    next_text = wordsegment.clean(text)
    word_list = []

    while len(next_text) > limit:
        current_text = next_text[:limit]
        next_text = next_text[limit:]
        word_list.extend(wordsegment.segment(current_text))
        next_text = ''.join([word_list[i] for i in xrange(-5, 0)]) + next_text
        word_list = word_list[:-5]
        gc.collect()

    word_list.extend(wordsegment.segment(next_text))
    text = ' '.join(w for w in word_list)
    return text


