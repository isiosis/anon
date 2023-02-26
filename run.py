# import openai

# openai.api_key = "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"

# engines = openai.Engine.list()

# print(engines)

# completion = openai.Completion.create(
#     engine="text-babbage-001", prompt="Hello world")

# print(completion)

from flask import Flask, render_template, request, send_file, jsonify
import os


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    pdf_url = f"/pdf/{file.filename}"
    return jsonify({'pdf_url': pdf_url})


@app.route('/pdf/<filename>')
def pdf(filename):
    return send_file(os.path.join(os.getcwd(), filename), mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
