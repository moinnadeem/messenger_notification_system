import redis

class MessengerBot():
	def __init__(self):
		self.r = redis.StrictRedis(host="localhost", db=1)
		self.p = self.r.pubsub()
	def notify(self, message):
		self.r.publish("notification", message)
	def update_status(self, status):
		self.r.set("status", status)	 
