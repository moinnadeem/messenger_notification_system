from flask import Flask, request
from pymessenger.bot import Bot

import redis

app = Flask(__name__)
r = redis.StrictRedis(host="localhost", db=1)
p = r.pubsub()

PAGE_ACCESS_TOKEN = # PAGE ACCESS TOKEN HERE
VERIFY_TOKEN = # VERIFY TOKEN HERE 
bot = Bot(PAGE_ACCESS_TOKEN)

RECIPIENT_ID = # YOUR FACEBOOK ID HERE


def handle_notification(message):
	bot.send_text_message(MOIN_RECIPIENT_ID, message['data'])
	
p.subscribe(**{"notification": handle_notification})

thread = p.run_in_thread(sleep_time=1)

@app.route("/", methods=['GET', 'POST'])
def hello():
	if request.method == 'GET':
		if request.args.get("hub.verify_token") == VERIFY_TOKEN:
			return request.args.get("hub.challenge")
		else:
			return 'Invalid verification token'
	if request.method == 'POST':
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for x in messaging:
				if x.get('message'):
					recipient_id = x['sender']['id']
					if recipient_id==MOIN_RECIPIENT_ID:
						status = r.get("status")
						bot.send_text_message(recipient_id, status)
					else:
						bot.send_text_message(recipient_id, "Please contact Moin to use this bot.")
				else:
					pass
		return "Success"

if __name__ == "__main__":
	app.run(port=5002, debug=True)
