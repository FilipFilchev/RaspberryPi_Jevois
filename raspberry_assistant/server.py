from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium", padding_side='left')
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

@app.route('/home')
def home():
    return jsonify(message="Hello World! Welcome to my post requests pi communication server")

@app.route('/secret')
def lachy():
    return "This is secret!"

@app.route('/dialogpt', methods=['POST'])
def dialogpt():
    text = request.json['text']
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    response_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



"""For multithreading:
To run this Flask app with Gunicorn, you'd use a command like:
gunicorn -w 4 -b 0.0.0.0:5000 server:app
or 2 instead of 4
"""