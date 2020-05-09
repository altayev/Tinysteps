from flask import Flask, render_template, request
import data
import json
import random
from forms import BookingForm, RequestForm


app = Flask(__name__)
app.secret_key = 'Developer' #TODO Скрыть этот ключ в переменной окружения в .env


def convert_data_to_json():
	teachers = data.teachers
	with open("teachers.json", "w", encoding='utf8') as f:
		json.dump(teachers, f, ensure_ascii=False)

	goals = data.goals
	with open("goals.json", "w", encoding='utf8') as f:
		json.dump(goals, f, ensure_ascii=False)

	days = data.days
	with open("days.json", "w", encoding='utf8') as f:
		json.dump(days, f, ensure_ascii=False)


def create_databases():
	with open("bookings.json", "w", encoding='utf8') as f:
		json.dump([{}], f, ensure_ascii=False)

	with open("requests.json", "w", encoding='utf8') as f:
		json.dump([{}], f, ensure_ascii=False)


@app.route('/')
def render_index():
	with open("teachers.json", "r") as f:
		teachers = json.load(f)

	with open("goals.json", "r") as f:
		goals = json.load(f)


	random.shuffle(teachers)

	return render_template(
		'index.html',
		teachers=teachers,
		goals=goals,
	)


@app.route('/all')
def render_all():
	with open("teachers.json", "r") as f:
		teachers = json.load(f)

	with open("goals.json", "r") as f:
		goals = json.load(f)

	return render_template(
		'all.html',
		teachers=teachers,
		goals=goals,
	)


@app.route('/goals/<goal>')
def render_goal(goal):
	with open("teachers.json", "r") as f:
		teachers = json.load(f)

	with open("goals.json", "r") as f:
		goals = json.load(f)

	teachers = [teacher for teacher in teachers if goal in teacher['goals']]

	goal_text = goals[goal].split(' ')[-1]
	goal_emoji = goals[goal].split(' ')[0]

	return render_template(
		'goal.html',
		teachers=teachers,
		goals=goals,
		goal_text=goal_text,
		goal_emoji=goal_emoji,
	)


@app.route('/profiles/<profile_id>')
def render_profile(profile_id):
	with open("teachers.json", "r") as f:
		teachers = json.load(f)

	with open("goals.json", "r") as f:
		goals = json.load(f)

	with open("days.json", "r") as f:
		days = json.load(f)

	teacher = [teacher for teacher in teachers if teacher['id'] == int(profile_id)][0]

	teacher_time = teacher['free']

	return render_template(
		'profile.html',
		teacher=teacher,
		goals=goals,
		teacher_time=teacher_time,
		days=days,
	)


@app.route('/booking/<profile_id>/<day>/<time>/')
def render_booking(profile_id, day, time):
	with open("teachers.json", "r") as f:
		teachers = json.load(f)

	with open("days.json", "r") as f:
		days = json.load(f)

	teacher = [teacher for teacher in teachers if teacher['id'] == int(profile_id)][0]

	teacher_name = teacher['name']
	teacher_pic = teacher['picture']
	teacher_id = teacher['id']
	day = days[day]
	time = time.replace("-", ":")

	form = BookingForm()

	return render_template(
		'booking.html',
		teacher_name=teacher_name,
		teacher_pic=teacher_pic,
		teacher_id=teacher_id,
		day=day,
		time=time,
		form=form,
	)


@app.route('/booking_done/', methods=["POST"])
def render_booking_done():
	form = BookingForm()
	name = form.name.data
	phone = form.phone.data
	day = form.day.data
	time = form.time.data
	teacher_id = form.teacher_id.data
	teacher_name = form.teacher_name.data

	with open("bookings.json", "r", encoding='utf8') as f:
		bookings = json.load(f)

	booking_info = {
		'client_id': len(bookings) + 1,
		'client_name': name,
		'client_phone': phone,
		'booking_date': f"{day},{time}",
		'booking_teacher': f"{teacher_name} (ID:{teacher_id})",
	}

	bookings.append(booking_info)

	with open("bookings.json", "w", encoding='utf8') as f:
		json.dump(bookings, f, ensure_ascii=False)


	return render_template(
		'booking_done.html',
		form=form,
		name=name,
		phone=phone,
		day=day,
		time=time,
	)


@app.route('/request/')
def render_request():
	form = RequestForm()

	return render_template(
		'request.html',
		form=form,
	)


@app.route('/request_done/', methods=["POST"])
def render_request_done():
	form = RequestForm()

	with open("requests.json", "r", encoding='utf8') as f:
		requests = json.load(f)

	requests_info = {
		'client_id': len(requests) + 1,
		'client_name': form.name.data,
		'client_phone': form.phone.data,
		'client_hours': form.have_hours.data,
		'client_goal': form.goal.data,
	}

	requests.append(requests_info)

	with open("requests.json", "w", encoding='utf8') as f:
		json.dump(requests, f, ensure_ascii=False)

	return render_template(
		'request_done.html',
		form=form,
	)


@app.route('/crm_bookings/')
def render_crm_bookings():
	with open("bookings.json", "r") as f:
		bookings = json.load(f)

	return render_template(
		'crm_bookings.html',
		bookings=bookings,
	)



convert_data_to_json()
create_databases()

if __name__ == '__main__':
	app.run()
