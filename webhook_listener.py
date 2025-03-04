from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/github-webhook/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Run the deployment script
        subprocess.call(["/home/ec2-user/site/HaaretzMusafim/scripts/deploy.sh"])
        return "Webhook received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
