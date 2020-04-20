import pickle
from os.path import isfile

import numpy as np
import variables_and_functions as vaf

import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return '''Welcome to the text classifer from ONU_FOR_NBU team!
           Here you can analyze your document (Txt files are preferred):
            <form action="http://text-classifier-onu-for-nbu.herokuapp.com/analyze_doc" method="post" enctype="multipart/form-data"> <input type="file" name="file"> <input type="submit"> </form>
           Or to learn our machine on your data (Our program needs a ZIP-folder with foloders(categores) in it, which contain data (txt documents)):
            <form action="http://text-classifier-onu-for-nbu.herokuapp.com/learn" method="post" enctype="multipart/form-data"> <input type="file" name="file"> <input type="submit"> </form> 
          Please, send zip-archive that contains one directory that contains directory-categories with txt files within.
          Good luck!'''

def analyze():
    print(10)
    f = open(vaf.analyzingfile, 'r')
    X = f.readlines()
    f.close()
    print(11)
    documents = vaf.text_preprocessing(X)

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidfconverter = TfidfVectorizer()
    try:
        X = tfidfconverter.fit_transform(documents).toarray()
    except Exception:
        return "Undefined category"

    ar = [0] * (vaf.maxfeatures - len(X[0]))
    X = [np.concatenate((X[0], ar))]

    from sklearn.feature_extraction.text import TfidfTransformer
    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    ar = [0] * (vaf.maxfeatures - len(X[0]))
    X = [np.concatenate((X[0], ar))]

    with open('text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)
    res = model.predict(X)
    return 'Category# ' + res[0]


from django import *


@app.route('/analyze_doc', methods=['POST', 'PUT'])
def analyze_doc():
    from django.http import HttpResponseRedirect
    from os import path
    print("document is received")
    try:
        file = request.files[u'file']
        print("file is received")
    except Exception:
        print("document is not available")
        return "Wrong file"
        print(file.readlines())
    #print(file.filename)
    f=open(vaf.analyzingfile,'w')
    for s in file.readlines():
        f.write(s)
    f.close()
    print("sucsess")
    return analyze(), 200

@app.route('/learn', methods=['POST', 'PUT'])
def learn():
    import zipfile
    import os
    try:
        data = zipfile.ZipFile(request.files[u'file'])
    except Exception:
        return "Wrong file"
    print("file is geted")

    import shutil
    shutil.rmtree("Data")
    data.extractall("Data")
    learndata = os.listdir("Data")

    print("Old data is cleaned")

    if os.path.exists("Data/" + learndata[0]) and len(learndata) == 1:
        print("data is available")
        import machine
        machine.learn("Data/" + learndata[0])
        print("machine is learned")
        # clean data directory
        import shutil
        shutil.rmtree("Data/" + learndata[0])
        return "Model is trained", 200
    else:
        import shutil
        shutil.rmtree("Data/" + learndata[0])
        return "Please, send zip-archive that contains one directory that contains directory-categories with txt files within", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    print("listening is started")