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
			errors['uname'] = 'Username must be a minimum of 5 characters'
		if User.objects.filter(username = postData['uname'].lower()).exists():
			errors['exists'] = 'Username already in use'
		if not name_regex.match(postData['uname']):
			errors['letters'] = 'Username must only contain letters and numbers'
		if len(postData['pword']) < 8:
			errors['pword'] = 'Password must be a minimum of 8 characters'
		if not postData['pword'] == postData['cpword']:
			errors['cpword'] = 'Passwords do not match'
		if len(errors) == 0:
			pw = bcrypt.hashpw(postData['pword'].encode(), bcrypt.gensalt())
			newuser = User.objects.create(username = postData['uname'], pword = pw)
			errors['id'] = newuser.id
		return errors

	def login_validator(self, postData):
		errors = {}
		if len(postData['uname']) < 1:
			errors['uname'] = 'Username field was left blank'
		if len(postData['pword']) < 1:
			errors['pword'] = 'Password field was left blank'
		if len(errors) == 0:
			if User.objects.filter(username = postData['uname']).exists():
				user = User.objects.get(username = postData['uname'])
				if bcrypt.checkpw(postData['pword'].encode(), user.pword.encode()):
					errors['id'] = user.id
				else:
					errors['credentials'] = "Wrong credentials"
			else:
				errors['credentials'] = "Wrong credentials"
		return errors

	def msg_validator(self, postData):
		errors = {}
		if len(postData['msg']) < 1:
			errors['msg'] = "Message is empty"
		if len(errors) == 0:
			Message.objects.create(content = postData['msg'], created_at = datetime.now(), sender_id = postData['uid'], conversation_id = postData['tid'])	
			errors['success'] = "Success"
		return errors

	def update_validator(self, postData):
		errors = {}
		values = {}
		user = User.objects.get(id = postData['uid'])
		if len(postData['desc']) > 0:
			if len(postData['desc']) < 10:
				errors['desc'] = "Description must be a minimum of 10 characters"
			else:
				user.desc = postData['desc']
				user.save()
				errors['desc'] = "Description successfully saved"

		if len(postData['year']) > 0:
			if int(postData['year']) > 2019:
				errors['year'] = "Are you a time traveler?"
			elif int(postData['year']) < 1940:
				errors['year'] = "Are you sure that car has an internal combustion engine?"
			else:
				user.year = int(postData['year'])
				user.save()
				errors['year'] = "Year successfully saved"

		if len(postData['model']) > 0:
			if len(postData['model']) < 2:
				errors['model'] = "Invalid model"
			else:
				user.model = postData['model']
				user.save()
				errors['model'] = "Model successfully saved"

		if len(postData['make']) > 0:
			if len(postData['make']) < 3:
				errors['make'] = "Invalid make"
			else:
				user.make = postData['make']
				user.save()
				errors['make'] = "Make successfully saved"

		if len(postData['power']) > 0:
			if int(postData['power']) < 100:
				errors['power'] = "U seriously in this app with that power?"
			elif int(postData['power']) > 2000:
				errors['power'] = "You car is too op"
			else:
				user.power = int(postData['power'])
				user.save()
				errors['power'] = "Power successfully saved"

		if len(postData['weight']) > 0:
			if int(postData['weight']) < 1:
				errors['weight'] = "Invalid weight"
			else:
				user.weight = postData['weight']
				user.save()
				errors['weight'] = "Weight successfully saved"

		if not postData['dtrain'] == "choose":
			user.dtrain = postData['dtrain']
			user.save()
			errors['dtrain'] = "Drivetrain successfully saved"

		return errors

	def loc_valid(self, postData): #for saving the location and making a message that a location was saved.
		convo = Conversation.objects.get(id = postData['cid'])
		convo.latitude = postData['long']
		convo.longitude = postData['lat']
		convo.latitude2 = postData['long2']
		convo.longitude2 = postData['lat2']
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
	longitude2 = models.FloatField(default = 37.3753997)
	latitude2 = models.FloatField(default = -121.9123471)

class Message(models.Model):
	"""docstring for Message"""
	content = models.CharField(max_length = 255)
	created_at = models.DateTimeField()
	sender = models.ForeignKey(User, related_name = "sent_msgs")
	conversation = models.ForeignKey(Conversation, related_name = "messages")
		
		