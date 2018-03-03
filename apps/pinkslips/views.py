from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.utils.timezone import now

def index(request): #render root page
	return render(request, 'pinkslips/signin.html')

def signin(request): #home page
	return render(request, 'pinkslips/home.html')

def log(request): #log in
	if request.method == "POST":
		errors = User.objects.login_validator(request.POST)
		if 'id' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/')
		else:
			request.session['id'] = errors['id']
			return redirect('/home')
	return redirect('/')

def create(request): # render register page
	return render(request, 'pinkslips/register.html')

def register(request): # registration 
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if 'id' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/create')
		else:
			request.session['id'] = errors['id']
			print request.session['id']
			return redirect('/edit')
	return redirect('/create')

def home(request): #home page
	if 'id' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id = request.session['id']) #user object


		#display users to like or dislikee
		userfilter = User.objects.exclude(id = request.session['id']).exclude(haters = user).exclude(likers = user)


		#get all matches
		check1 = Conversation.objects.all()
		matchedusers = []
		if len(check1):
			for i in check1:
				if user.id == i.speaker1_id:
					matchedusers.append(i.speaker2)
				elif user.id == i.speaker2_id:
					matchedusers.append(i.speaker1)

		#used in the header
		# ex: matches(2)
		request.session['num'] = len(matchedusers)

		#removing list of matched users from userfilter
		res = list(set(matchedusers)^set(userfilter))


		if len(res) == 0: #reset list
			user.disliked_users.clear()
			user.liked_users.clear()
			return redirect('/home')
		else:
			opponent = res[0]
			request.session['opponent_id'] = opponent.id
			context = {
				'user': user,
				'opponent': opponent,
			}
	return render(request, 'pinkslips/home.html', context)

def profile(request): #show user profile
	if 'id' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id = request.session['id'])
		context = {
			'user': user,
		}
	return render(request, 'pinkslips/profile.html', context)

def edit(request): #render edit page
	if 'id' not in request.session:
			return redirect('/')
	return render(request, 'pinkslips/editp.html')

def update(request): #update profile info
	if request.method == "POST":
		errors = User.objects.update_validator(request.POST)
		if 'status' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/edit')
		else:
			return redirect('/edit')
	pass

def upload(request): #upload img url which has a default value for now
	if request.method == "POST":
		user = User.objects.get(id = request.session['id'])
		user.url = request.POST['pic']
		user.save()
		return redirect('/profile')
		pass

def dislike(request): #dislike user query
	if 'id' not in request.session:
		return redirect('/')
	else:
		from_user = User.objects.get(id = request.session['id'])
		to_user = User.objects.get(id = request.session['opponent_id'])
		from_user.disliked_users.add(to_user)
		return redirect('/home')

def like(request): #like user query
	if 'id' not in request.session:
		return redirect('/')
	else:
		from_user = User.objects.get(id = request.session['id'])
		to_user = User.objects.get(id = request.session['opponent_id'])
		from_user.liked_users.add(to_user)
		liked_users = from_user.liked_users.all()
		# code for each time you like. it will check if it liked you back
		for user in liked_users:
			i = user.liked_users.all()
			for user2 in i:
				if user2 == from_user:
					match = Conversation.objects.create(speaker1_id = from_user.id, speaker2_id = user.id)
					from_user.liked_users.remove(to_user)
					to_user.liked_users.remove(from_user)
					return redirect('/newmatch')
		return redirect('/home')

def newmatch(request): #notification that u matched w someone
	if 'id' not in request.session:
		return redirect('/')
	else:
		return render(request, 'pinkslips/newmatch.html')

def logout(request):
	request.session.clear()
	return redirect('/')

def matches(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		#get all matches to render on page
		user = User.objects.get(id = request.session['id'])
		check1 = Conversation.objects.all()
		convo = []
		if len(check1):
			for i in check1:
				if user.id == i.speaker1_id:
					convo.append(i)
				elif user.id == i.speaker2_id:
					convo.append(i)
		context = {
			'user': user,
			'convo': convo
		}
		return render(request, 'pinkslips/match.html', context)
	return redirect('/home')

def thread(request, tid):
	if 'id' not in request.session:
		return redirect('/')
	else:
		#display msgs
		user = User.objects.get(id=request.session['id'])
		convo = Conversation.objects.filter(id = tid)
		msgs = Message.objects.filter(conversation_id = tid)
		if len(convo) == 0:
			return redirect('/')
		else:
			convo = convo[0]
			context = {
				'convo': convo,
				'user': user,
				'msgs': msgs
			}
			if convo.speaker1 == user:
				return render(request, 'pinkslips/marker2test.html', context)
			elif convo.speaker2 == user:
				return render(request, 'pinkslips/marker2test.html', context)
			else:
				return redirect('/')
	return redirect('/matches')

def pstmsg(request):
	if request.method == "POST":
		#Posting a message
		num =  request.POST['tid']
		errors = User.objects.msg_validator(request.POST)
		if 'success' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/thread/' + num)
		else:
			return redirect('/thread/' + num)
	return redirect('/matches')

def savemap(request):
	if request.method == "POST":
		User.objects.loc_valid(request.POST)
		return redirect('/thread/' + request.POST['cid'])
	pass












def cartest(request):
	return render (request, 'pinkslips/car.html')