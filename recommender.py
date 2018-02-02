import mysqlconnect
import nltk
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import itertools

cnx = mysqlconnect.connect()

cursor = cnx.cursor()

query = ("SELECT comment, label FROM `restaurant_comments_labled_as_rating` ")

cursor.execute(query);

reviews = []
for review in cursor:
    reviews.append(review)
    
dataset = np.array(reviews)

words = [word_tokenize(w[0]) for w in dataset]
words = list(itertools.chain.from_iterable(words))

all_words = nltk.FreqDist(word.lower() for word in words)

print('extracting words!')
word_features = [i for i, j in all_words.most_common()][:100]
print(len(word_features))


def review_features(review): 
    review_words = set(review) 
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in review_words)
#    print('review', review)
    return features


X = dataset[:, 0:-1]
y = dataset[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

print('extracting features!')
X_train_dict = [review_features(word_tokenize(x[0])) for x in X_train]
X_test_dict = [review_features(word_tokenize(x[0])) for x in X_test]

#print(X_test_dict[500], y_test[500])

print('will now start to classify')
classifier = nltk.NaiveBayesClassifier.train(list(zip(X_train_dict, y_train)))


print('classification done')
print('Accuracy: ', 100* nltk.classify.accuracy(classifier, list(zip(X_test_dict, y_test))))

classifier.show_most_informative_features(5)

import pickle
f = open('recommender-review-classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()



mysqlconnect.close(cnx)
