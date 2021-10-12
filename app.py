import numpy as np
from PIL import Image
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import random


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)








app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def random_image_number():
    return str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    num = random_image_number()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = num + secure_filename(file.filename)
            file.save(os.path.join("static", filename))
            return redirect(url_for('result',filename=filename))
    return render_template("upload.html")



@app.route("/result/<filename>")
def result(filename):
    path = "./static/" + filename
    imgarr = Image.open(path)
    img = np.array(imgarr)
    unqc, C = np.unique(img.reshape(-1, img.shape[-1]), axis=0, return_counts=True)
    topNidx = np.argpartition(C, -10)[-10:]
    a = unqc[topNidx]
    b = C[topNidx]

    indices = b.argsort()

    list_1 = a[indices]
    list_2 = b[indices]
    percent = []
    lena = np.sum(list_2)

    for i in list_2:
        per = ((i / (lena)) * 100)
        per = round(per, 2)
        percent.append(per)


    # os.remove(path)
    list_3 = []
    hex_list = []
    for i in range(10):
        list_3.append((list_1[i][0],list_1[i][1],list_1[i][2]))

    for i in range(10):
        triplet = rgb_to_hex(list_3[i])
        hex_list.append(triplet)

    new_path = path[9:]



    return render_template("result.html", tuples=list_3,percent=percent,hex = hex_list,path=new_path)




if __name__ == "__main__":
    app.run(debug=True)




