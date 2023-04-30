import openai, os, requests
from flask import Flask, render_template, redirect, url_for, request

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/ai')
def index():
    return render_template('index.html')  

@app.route('/ai/create',methods = ['POST', 'GET'])
def play():
   if request.method == 'POST':
      prompt = request.form['prompt']
      return redirect(url_for('show_image', command = prompt))
      
@app.route('/ai/<command>')
def show_image(command):
   response = openai.Image.create(
      prompt=command,
      n=1,
      size="256x256",
      response_format="url"
   )
   image_url = response['data'][0]['url']

   # A placeholder image for the UI testing since API access costs $$
   #image_url = "https://images.unsplash.com/photo-1559253664-ca249d4608c6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZnJvZ3xlbnwwfHwwfHw%3D&auto=format&fit=crop&w=600&q=60"
   response = requests.get(image_url)
   filename = os.path.join(app.static_folder, 'fetched_image.png')
   with open(filename, 'wb') as f:
        f.write(response.content)
   return render_template('index.html', image='fetched_image.png', prompt=command)   
   