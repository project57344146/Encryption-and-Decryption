from flask import Flask, request, render_template
from PIL import Image
import numpy as np
import base64
import io

app = Flask(__name__)

# Convert image array → base64 (for display)
def to_base64(img_array):
    img = Image.fromarray(img_array.astype('uint8'))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    key = int(request.form['key'])
    action = request.form['action']

    image = Image.open(file).convert('RGB')
    img_array = np.array(image)

    # XOR works for both encryption & decryption
    result_array = img_array ^ key

    original_img = to_base64(img_array)
    result_img = to_base64(result_array)

    # Show only 5x5 sample pixels
    original_pixels = img_array[:5, :5].tolist()
    result_pixels = result_array[:5, :5].tolist()

    return render_template(
        'index.html',
        original_img=original_img,
        result_img=result_img,
        original_pixels=original_pixels,
        result_pixels=result_pixels,
        action=action
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)