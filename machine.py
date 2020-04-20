from variables_and_functions import *

def learn(learndata):
    import numpy as np
    import nltk
    from sklearn.datasets import load_files
    from sklearn.ensemble import RandomForestClassifier

    nltk.download('stopwords')
    import pickle
    from nltk.corpus import stopwords

    movie_data = load_files(learndata)
    X, y = movie_data.data, movie_data.target

    documents=text_preprocessing(X)

    from sklearn.feature_extraction.text import TfidfVectorizer

    tfidfconverter = TfidfVectorizer(max_features=maxfeatures, min_df=mindf, max_df=maxdf, stop_words=stopwords.words('english'))
    X = tfidfconverter.fit_transform(documents).toarray()

    from sklearn.feature_extraction.text import TfidfTransformer
    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsize, random_state=randomstate)

    classifier = RandomForestClassifier(n_estimators=nestimators, random_state=randomstate)
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    print(accuracy_score(y_test, y_pred))

    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(classifier,picklefile)