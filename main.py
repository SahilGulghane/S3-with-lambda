import time
from boto3 import Session
from flask import *
import boto3
import json
from botocore.exceptions import NoCredentialsError
import var
app = Flask(__name__)
app = Flask(__name__, template_folder='../templates')
@app.route('/')
def main():
	return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)


		ACCESS_KEY = var.ACCESS_KEY
		SECRET_KEY = var.SECRET_KEY

		def upload_to_aws(local_file, bucket, s3_file):
			s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
							  aws_secret_access_key=SECRET_KEY)

			try:
				s3.upload_file(local_file, bucket, s3_file)
				print("Upload Successful")
				return True
			except FileNotFoundError:
				print("The file was not found")
				return False
			except NoCredentialsError:
				print("Credentials not available")
				return False

		uploaded = upload_to_aws(f.filename, 'myaudiobucket4545', f.filename)
		time.sleep(30)

		session = Session(aws_access_key_id=ACCESS_KEY,
						  aws_secret_access_key=SECRET_KEY)
		s3 = session.resource('s3')
		your_bucket = s3.Bucket('myaudiobucket4545')

		for s3_file in your_bucket.objects.all():
			print(s3_file.key)  # prints the contents of bucket

		s3 = boto3.client('s3')

		s3.download_file('myaudiobucket4545', 'transcripts/'+f.filename+'-transcript.json', 'E:\dow/' +f.filename+'.txt')
		f1 = open('E:\dow/' + f.filename + '.txt')

		# returns JSON object as
		# a dictionary
		data = json.load(f1)
		xyz = data['results']['transcripts']
		# Closing file
		f1.close()
		return  render_template("Acknowledgement.html", name=f.filename,filename='E:\dow/' +f.filename+'.txt' , text= xyz )









if __name__ == '__main__':
    app.run(debug=True)
