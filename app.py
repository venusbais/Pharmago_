import os
import shutil

import scrapperfile as sc
from flask import Flask, render_template, redirect, url_for
from flask import request
from werkzeug.utils import secure_filename
from google.cloud import vision
import io
import json
# import src.modelcaller as smod
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'mygooglekey.json'

app = Flask(__name__)

dataa = []

@app.route('/', methods = ['GET', 'POST'])
def test_get():
    if request.method == 'POST':
        file = request.files['file']
        # if allowed_file(file.filename) == True:
        # temp_name = secure_filename(file.filename.replace(" ", ""))
        file.save(secure_filename(file.filename.replace(" ", "")))

        shutil.move(r"./word.png", r"../data/word.png")
        print("just moved the filee and will attempt to redirect")
        return redirect(url_for('results_displayer'))

    else:
        return render_template("index.html")


@app.route("/results")
def results_displayer():
    print("was able to redirect and now preparing to render")
    data_to_insert = [
        [(14.42, 'Dolo 500mg Tablet', 'https://pharmeasy.in/online-medicine-order/dolo-500mg-tablet-19749'),
         (17.51, 'Paracip 650mg Tablet', 'https://pharmeasy.in/online-medicine-order/paracip-650mg-tablet-6878'),
         (19.42, "P 650mg Tablets 10'S", 'https://pharmeasy.in/online-medicine-order/p-650mg-tab-10-s-169787')],
        [(14.73, "Crocin Tablet 10's", 'https://www.apollopharmacy.in/otc/crocin-tablet-10-s?doNotTrack=true'),
         (16.97, "Crocin 500 mg Tablet 15's", 'https://www.apollopharmacy.in/otc/crocin-500mg-tablet?doNotTrack=true'),
         (18.4, "Paracetamol 500 Tablet 10's",
          'https://www.apollopharmacy.in/otc/paracetamol-500mg-tab-10-s-kaithy?doNotTrack=true')]]

    # data_to_insert= sc.master_scrapper("crocin")
    # REMEMBER THAT YOU HAVE TO LINK THE MODELS OUTPUT HERE. PARACETAMOL IS JUST A PLACE HOLDER FOR NOW.'''



    client = vision.ImageAnnotatorClient()

    with io.open("../data/word.png", 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    anssssss=''
    for i in texts:
        if i.description !="":
            anssssss=anssssss+str(i.description)
            break
        # print((i.description))
        # # print('\n"{}"'.format(i.description))
        # anssssss=anssssss+'\n"{}"'.format(i.description)
    print('we done boiiiii')
    print("[",anssssss,"]")

    # a = smod.modelcallerandtextreturner()
    # finans = sc.response_corrector(a)
    finans = anssssss
    print(finans)
    print("wassup")
    global dataa
    dataa = sc.master_scrapper(finans)
    data_to_insert = dataa
    print(dataa)
    return render_template("finalpage.html", data_to_insert=data_to_insert)

if __name__ == "__main__":
    app.debug = True
    app.run()
