maxfeatures = 1500
mindf = 5
maxdf = 0.7
testsize = 0.2
nestimators = 1000
randomstate = 0
analyzingfile="analyzing_file.txt"
def text_preprocessing(movie_data):
    import re
    documents = []

    import nltk
    nltk.download('wordnet')
    from nltk.stem import WordNetLemmatizer

    stemmer = WordNetLemmatizer()

    for sen in range(0, len(movie_data)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(movie_data[sen]))

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)

        documents.append(document)
    return documents