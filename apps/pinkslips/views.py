from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.utils.timezone import now

def index(request):
	return render(request, 'pinkslips/signin.html')

def signin(request):
	return render(request, 'pinkslips/home.html')

def log(request):
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

def create(request):
	return render(request, 'pinkslips/register.html')

def register(request):
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

def home(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id = request.session['id'])
		userfilter = User.objects.exclude(id = request.session['id']).exclude(haters = user).exclude(likers = user)

		check1 = Conversation.objects.all()
		matchedusers = []
		if len(check1):
			for i in check1:
				if user.id == i.speaker1_id:
					matchedusers.append(i.speaker2)
				elif user.id == i.speaker2_id:
					matchedusers.append(i.speaker1)

		request.session['num'] = len(matchedusers)

		res = list(set(matchedusers)^set(userfilter))

		if len(res) == 0:
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

def profile(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id = request.session['id'])
		context = {
			'user': user,
		}
	return render(request, 'pinkslips/profile.html', context)

def edit(request):
	return render(request, 'pinkslips/editp.html')

def update(request):
	if request.method == "POST":
		errors = User.objects.update_validator(request.POST)
		if 'status' not in errors:
			for tag, error in errors.iteritems():
				messages.error(request,error, extra_tags = tag)
			return redirect('/edit')
		else:
			return redirect('/edit')
	pass

def upload(request):
	if request.method == "POST":
		user = User.objects.get(id = request.session['id'])
		user.url = request.POST['pic']
		user.save()
		return redirect('/profile')
		pass

def dislike(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		from_user = User.objects.get(id = request.session['id'])
		to_user = User.objects.get(id = request.session['opponent_id'])
		from_user.disliked_users.add(to_user)
		return redirect('/home')

def like(request):
	if 'id' not in request.session:
		return redirect('/')
	else:
		from_user = User.objects.get(id = request.session['id'])
		to_user = User.objects.get(id = request.session['opponent_id'])
		from_user.liked_users.add(to_user)
		liked_users = from_user.liked_users.all()
		for user in liked_users:
			i = user.liked_users.all()
			for user2 in i:
				if user2 == from_user:
					match = Conversation.objects.create(speaker1_id = from_user.id, speaker2_id = user.id)
					from_user.liked_users.remove(to_user)
					to_user.liked_users.remove(from_user)
					return redirect('/newmatch')
		# insert code if 2 users like each other, redirect to matches
		# page and instatiate message that says user x and user y matched
		return redirect('/home')

def newmatch(request):
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
				return render(request, 'pinkslips/map.html', context)
			elif convo.speaker2 == user:
				return render(request, 'pinkslips/map.html', context)
			else:
				return redirect('/')
	return redirect('/matches')

def pstmsg(request):
	if request.method == "POST":
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



