# CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# with open('../DataPreprocessing/processed_data.csv','r') as inputdata, open('source_data.txt','a') as outputfile:
#     for line in inputdata:
#         outputfile.write(line.rstrip('\n').split(',')[1]+'\n')

with open('/home/jarvisr/Datasets/source_data.txt','r') as data:
    train_data = [line.strip('\n') for line in data]

count_vect = CountVectorizer(min_df=1)
X_train_counts = count_vect.fit_transform(train_data)
print X_train_counts.shape
# print count_vect.vocabulary_.get(u'search')
