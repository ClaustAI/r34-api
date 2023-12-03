from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/s/<prompt>')
def get_images(prompt):
    url = f'https://rule34.us/index.php?r=posts/index&q={prompt}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_src_array = []
    for a in soup.select('.thumbail-container a'):
        img_url = a['href']
        img_response = requests.get(img_url)
        img_soup = BeautifulSoup(img_response.text, 'html.parser')
        img_src = img_soup.select_one('.content_push img')['src']
        if img_src.endswith('.png') or img_src.endswith('.jpeg') or img_src.endswith('.jpg'):
            img_src_array.append(img_src)

    return jsonify(img_src_array)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
