from flask import Flask
from flask import render_template, request, url_for
from werkzeug.utils import secure_filename
import subprocess




app = Flask(__name__)

@app.route("/")
def root():
    return render_template('content.html')



@app.route('/file-upload', methods=['POST'])
def uploadFile():
    if request.method == 'POST':
    	f = request.files['file']
    	f.save('uploads/' + secure_filename(f.filename))
    	return 'true'


@app.route('/get_breed', methods=['POST'])
def getBreed():
	if request.method == 'POST':
		image_path = "uploads/{}".format(request.form['image_name'])
		command = ['python', 'model.py', image_path]
		p = subprocess.Popen(command, stdout=subprocess.PIPE)
		text = p.stdout.read()
		retcode = p.wait()
		return text
