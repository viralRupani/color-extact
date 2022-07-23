from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alksdfoaweiflsdkj'
app.config['UPLOAD_FOLDER'] = 'static/image/'


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filename = filename.replace(filename[:-4], 'image')
            file_format = filename.split('.')[1]
            if file_format == 'png':
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = Image.open('static/image/image.png')
                img = image.convert('RGB')
                img.save('static/image/image.jpg')
                os.remove('static/image/image.png')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_image'))
    return render_template('index.html')


@app.route('/show_image')
def show_image():
    with Image.open(f'static/image/image.jpg') as image:
        imagedata = np.asarray(image)
        setx = {tuple(imagedata[i][j]) for i in range(imagedata.shape[0]) for j in range(imagedata.shape[1])}
        list_ = [list(setx)[_] for _ in range(10)]
        hexcode = [rgb_to_hex(list_[_]) for _ in range(10)]
        color_dictionary = {key: value for (key, value) in zip(list_, hexcode)}
    return render_template('image.html', imagedata=imagedata, color_dictionary=color_dictionary)


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


if __name__ == "__main__":
    app.run(debug=True)
