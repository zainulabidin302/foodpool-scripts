import mysqlconnect
import nltk
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import itertools
from nltk import ngrams
from nltk.corpus import stopwords
import string


cnx = mysqlconnect.connect()

cursor = cnx.cursor()

query = ("SELECT comment, label FROM `restaurant_comments_labled_as_rating` ")

cursor.execute(query);

reviews = []
for review in cursor:
    reviews.append(review)

stop_words = list(set(stopwords.words('english')))
import sys

def remove_unwanted_chars(review):
    label  = review[1]
    _review = review[0]
    #_review = review.translate(str.maketrans('','',string.punctuation))
    _review = word_tokenize(_review)
    _review = [word for word in _review if word not in stop_words]
    
    return [_review, label]



dataset = np.array(list(map(remove_unwanted_chars, reviews)))

words = [w[0] for w in dataset]
words = list(itertools.chain.from_iterable(words))


bigram_words = [list(ngrams(w[0], 2)) for w in dataset]
bigram_words = list(itertools.chain.from_iterable(bigram_words))
bigram_words = [' '.join(w) for w in bigram_words]


trigram_words = [list(ngrams(w[0], 3)) for w in dataset]
trigram_words = list(itertools.chain.from_iterable(trigram_words))
trigram_words = [' '.join(w) for w in trigram_words]

fourgram_words = [list(ngrams(w[0], 4)) for w in dataset]
fourgram_words = list(itertools.chain.from_iterable(fourgram_words))
fourgram_words = [' '.join(w) for w in fourgram_words]


all_words = nltk.FreqDist(word.lower() for word in words)
all_bigram_words = nltk.FreqDist(word.lower() for word in bigram_words)
all_trigram_words = nltk.FreqDist(word.lower() for word in trigram_words)
all_fourgram_words = nltk.FreqDist(word.lower() for word in fourgram_words)

print('extracting words!')

word_features = [i for i, j in all_words.most_common()][:200]
bigram_features = [i for i, j in all_bigram_words.most_common()][:10]
trigram_features = [i for i, j in all_trigram_words.most_common()][:10]
fourgram_features = [i for i, j in all_fourgram_words.most_common()][:10]



word_features.extend(bigram_features) 
word_features.extend(trigram_features)
word_features.extend(fourgram_features)

def review_features(review): 
    review_words = review 
    bigrams = [' '.join(b) for b in ngrams(review, 2)]
    trigrams = [' '.join(b) for b in ngrams(review, 3)]
    fourgrams = [' '.join(b) for b in ngrams(review, 4)]
    
    review_words.extend(bigrams)
    review_words.extend(trigrams)
    review_words.extend(fourgrams)
    review_words = set(review_words)
    
    
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in review_words)
#    print('review', review)
    return features


X = dataset[:, 0:-1]
y = dataset[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

print('extracting features!')
X_train_dict = [review_features(x[0]) for x in X_train]
X_test_dict = [review_features(x[0]) for x in X_test]

#print(X_test_dict[500], y_test[500])

print('will now start to classify')
classifier = nltk.NaiveBayesClassifier.train(list(zip(X_train_dict, y_train)))


print('classification done')
print('Accuracy: ', 100* nltk.classify.accuracy(classifier, list(zip(X_test_dict, y_test))))

classifier.show_most_informative_features(20)

import pickle
f = open('recommender-review-classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()



mysqlconnect.close(cnx)
