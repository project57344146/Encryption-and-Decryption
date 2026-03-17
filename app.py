from flask import Flask, request, render_template
from PIL import Image
import base64
import io

app = Flask(__name__)

def to_base64(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def encrypt_decrypt(image, key):
    pixels = list(image.getdata())
    new_pixels = []

    for pixel in pixels:
        new_pixel = tuple([value ^ key for value in pixel])
        new_pixels.append(new_pixel)

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    return new_image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    key = int(request.form['key'])
    action = request.form['action']

    image = Image.open(file).convert('RGB')

    result_image = encrypt_decrypt(image, key)

    original_img = to_base64(image)
    result_img = to_base64(result_image)

    return render_template(
        'index.html',
        original_img=original_img,
        result_img=result_img,
        action=action
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)