from flask import Flask, render_template, request, url_for
import qrcode
from qrcode.image.pil import PilImage
from PIL import Image
import re
import os

app = Flask(__name__)

def sanitize_filename(url):
    return re.sub(r'\W+', '_', url)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        color = request.form['color']
        filename = sanitize_filename(url) + '.png'
        img = generate_qr_code(url, color)
        img_path = os.path.join('static', 'generated_qr_codes', filename)
        img.save(img_path, "PNG")
        return render_template('index.html', image_url=url_for('static', filename=f'generated_qr_codes/{filename}'))
    return render_template('index.html')

def generate_qr_code(url, color):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color="white").convert('RGBA')

    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)

    return img

if __name__ == '__main__':
    os.makedirs('static/generated_qr_codes', exist_ok=True)
    app.run(debug=True)
