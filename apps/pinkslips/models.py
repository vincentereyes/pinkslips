from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils.timezone import now
import re
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		name_regex = re.compile(r'^[a-zA-Z0-9]+$')
		errors = {}
		if len(postData['uname']) < 4:
			errors['uname'] = 'username field left blank. 5 or more characters required'
		if User.objects.filter(username = postData['uname'].lower()).exists():
			errors['exists'] = 'username already used'
		if not name_regex.match(postData['uname']):
			errors['letters'] = 'letters and numbers only for usernames please'
		if len(postData['pword']) < 8:
			errors['pword'] = 'password needs a minimum of 8 characters'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'passwords dont match'
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			newuser = User.objects.create(username = postData['uname'], pword = pw)
			errors['id'] = newuser.id
		return errors

	def login_validator(self, postData):
		errors = {}
		if len(postData['uname']) < 1:
			errors['uname'] = 'username field left blank'
		if len(postData['pword']) < 1:
			errors['pword'] = 'password field left blank'
		if len(errors) == 0:
			if User.objects.filter(username = postData['uname']).exists():
				user = User.objects.get(username = postData['uname'])
				if bcrypt.checkpw(postData['pword'].encode(), user.pword.encode()):
					errors['id'] = user.id
				else:
					errors['credentials'] = "Wrong Credentials"
			else:
				errors['credentials'] = "Wrong Credentials"
		return errors

	def msg_validator(self, postData):
		errors = {}
		if len(postData['msg']) < 1:
			errors['msg'] = "message is empty"
		if len(errors) == 0:
			Message.objects.create(content = postData['msg'], created_at = datetime.now(), sender_id = postData['uid'], conversation_id = postData['tid'])	
			errors['success'] = "success"
		return errors

	def update_validator(self, postData):
		errors = {}
		values = {}
		user = User.objects.get(id = postData['uid'])
		if len(postData['desc']) > 0:
			if len(postData['desc']) < 10:
				errors['desc'] = "desc needs more than 10 characters"
			else:
				user.desc = postData['desc']
				user.save()
				errors['desc'] = "description successfully saved"

		if len(postData['year']) > 0:
			if int(postData['year']) > 2019:
				errors['year'] = "you can't have a car from the future or past"
			elif int(postData['year']) < 1940:
				errors['year'] = "are you sure that car has an internal combustion engine?"
			else:
				user.year = int(postData['year'])
				user.save()
				errors['year'] = "year successfully saved"

		if len(postData['model']) > 0:
			if len(postData['model']) < 2:
				errors['model'] = "invalid model"
			else:
				user.model = postData['model']
				user.save()
				errors['model'] = "model successfully saved"

		if len(postData['make']) > 0:
			if len(postData['make']) < 3:
				errors['make'] = "invalid make"
			else:
				user.make = postData['make']
				user.save()
				errors['make'] = "make successfully saved"

		if len(postData['power']) > 0:
			if int(postData['power']) < 100:
				errors['power'] = "u seriously in this app with that power?"
			elif int(postData['power']) > 2000:
				errors['power'] = "dont you have a different car with usable power?"
			else:
				user.power = int(postData['power'])
				user.save()
				errors['power'] = "power successfully saved"

		if len(postData['weight']) > 0:
			if int(postData['weight']) < 1:
				errors['weight'] = "invalid weight"
			else:
				user.weight = postData['weight']
				user.save()
				errors['weight'] = "weight successfully saved"

		if not postData['dtrain'] == "choose":
			user.dtrain = postData['dtrain']
			user.save()
			errors['dtrain'] = "drivetrain successfully saved"

		return errors

	def loc_valid(self, postData): #for saving the location and making a message that a location was saved.
		convo = Conversation.objects.get(id = postData['cid'])
		convo.latitude = postData['long']
		convo.longitude = postData['lat']
		convo.save()
		setter = User.objects.get(id = postData['uid'])
		Message.objects.create(content = "Location saved by " + setter.username, created_at = datetime.now(), sender_id = postData['uid'], conversation_id = postData['cid'])
		pass



class User(models.Model):
	username = models.CharField(max_length = 255)
	pword = models.CharField(max_length = 255)
	year = models.IntegerField(default = 0)
	make = models.CharField(max_length = 255, default="")
	model = models.CharField(max_length = 255, default="")
	weight = models.IntegerField(default = 0)
	desc = models.TextField(default = "")
	power = models.IntegerField(default = 0)
	dtrain = models.CharField(max_length = 255, default = "")
	liked_users = models.ManyToManyField("self", symmetrical = False, related_name= "likers")
	disliked_users = models.ManyToManyField("self", symmetrical = False, related_name = "haters")
	url = models.TextField(default = "")
	objects = UserManager()

		
class Conversation(models.Model):
	speaker1 = models.ForeignKey(User, related_name = "conversations")
	speaker2 = models.ForeignKey(User, related_name = "conversations_2")
	longitude = models.FloatField(default = 37.37541248891094)
	latitude = models.FloatField(default = -121.91015303558203)

class Message(models.Model):
	"""docstring for Message"""
	content = models.CharField(max_length = 255)
	created_at = models.DateTimeField()
	sender = models.ForeignKey(User, related_name = "sent_msgs")
	conversation = models.ForeignKey(Conversation, related_name = "messages")
		
		