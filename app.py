import os

from flask import Flask, render_template
from sqlalchemy import func
from flask_migrate import Migrate

from forms import BookingForm, RequestForm
from models import *
from data import days


app = Flask(__name__)
app.secret_key = 'Developer' #TODO Скрыть этот ключ в переменной окружения в .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def render_index():
	return render_template(
		'index.html',
		teachers=Teacher.query.order_by(func.random()).limit(6).all(),
		goals=Goal.query.all(),
	)


@app.route('/all')
def render_all():
	return render_template(
		'all.html',
		teachers=Teacher.query.order_by(Teacher.rating.desc()).all(),
		goals=Goal.query.all(),
	)


@app.route('/goals/<goal>')
def render_goal(goal):
	goal_db = (db.session.query(Goal).filter(Goal.goal_slug == goal)).scalar()

	teachers = goal_db.teacher
	goal_full_text = goal_db.goal_text
	goal_emoji, *args, goal_text = goal_full_text.split(' ')

	return render_template(
		'goal.html',
		teachers=teachers,
		goals=Goal.query.all(),
		goal_text=goal_text,
		goal_emoji=goal_emoji,
	)


@app.route('/profiles/<profile_id>')
def render_profile(profile_id):

	teacher = Teacher.query.filter(Teacher.id == profile_id).scalar()
	slots = []
	for slug, weekday in days.items():
		times = []
		for slot in teacher.timeslots:
			if slot.weekday == slug:
				times.append(slot.time.strftime("%H:%M"))
		slot = {
			slug:times
		}
		slots.append(slot)
	return render_template(
		'profile.html',
		teacher=teacher,
		days=days,
		slots=slots,
	)


@app.route('/booking/<profile_id>/<day>/<time>/')
def render_booking(profile_id, day, time):

	teacher = Teacher.query.filter(Teacher.id == profile_id).scalar()

	teacher_name = teacher.name
	teacher_pic = teacher.picture
	time = time.replace("-", ":")
	timeslot = (Timeslot.query.filter(db.and_(Timeslot.teacher_id == int(profile_id), Timeslot.weekday == day, Timeslot.time == time))).scalar()
	timeslot_id = timeslot.id
	day = days[day]

	form = BookingForm()

	return render_template(
		'booking.html',
		teacher_name=teacher_name,
		teacher_pic=teacher_pic,
		teacher_id=profile_id,
		timeslot_id=timeslot_id,
		day=day,
		time=time,
		form=form,
	)


@app.route('/booking_done/', methods=["GET", "POST"])
def render_booking_done():
	form = BookingForm()

	if not form.phone.data:
		form = RequestForm()
		return render_template(
			'request.html',
			form=form,
		)

	name = form.name.data
	phone = form.phone.data
	day = form.day.data
	time = form.time.data
	teacher_id = form.teacher_id.data
	timeslot_id = form.timeslot_id.data

	if Student.query.filter(Student.phone == phone).scalar():
		student = Student.query.filter(Student.phone == phone).scalar()
	else:
		student = Student(name=name, phone=phone)
		db.session.add(student)
		db.session.commit()

	booking = Booking(student_id=student.id, teacher_id=teacher_id, timeslot_id=timeslot_id)
	db.session.add(booking)
	db.session.commit()

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


@app.route('/request_done/', methods=["GET", "POST"])
def render_request_done():
	form = RequestForm()

	if not form.phone.data:
		return render_template(
			'request.html',
			form=form,
		)

	name = form.name.data
	phone = form.phone.data
	have_hours = form.have_hours.data
	goal = form.goal.data

	if Student.query.filter(Student.phone == phone).scalar():
		student = Student.query.filter(Student.phone == phone).scalar()
	else:
		student = Student(name=name, phone=phone)
		db.session.add(student)
		db.session.commit()

	current_request = Request(student_id=student.id, goal=goal, have_time=have_hours)
	db.session.add(current_request)
	db.session.commit()

	return render_template(
		'request_done.html',
		form=form,
	)


@app.route('/all_bookings/')
def render_all_bookings():
	bookings = Booking.query.all()

	return render_template(
		'all_bookings.html',
		bookings=bookings,
	)


@app.route('/all_requests/')
def render_all_requests():
	all_requests = Request.query.all()

	return render_template(
		'all_requests.html',
		all_requests=all_requests,
	)


if __name__ == '__main__':
	app.run()

