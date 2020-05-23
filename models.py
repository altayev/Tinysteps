import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

teacher_goals_association = db.Table(
	'teacher_goals',
	db.Column('teacher_id', db.Integer, db.ForeignKey('teachers.id')),
	db.Column('goal_id', db.Integer, db.ForeignKey('goals.id')),
)


class Teacher(db.Model):
	__tablename__ = 'teachers'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String, nullable=True, unique=True)
	about = db.Column(db.Text)
	rating = db.Column(db.Float)
	picture = db.Column(db.String)
	price = db.Column(db.Numeric)
	timeslots = db.relationship('Timeslot', back_populates='teacher')
	bookings = db.relationship('Booking', back_populates='teacher')
	goals = db.relationship('Goal', secondary=teacher_goals_association, back_populates='teacher')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)


class Timeslot(db.Model):
	__tablename__ = 'timeslots'
	id = db.Column(db.Integer, primary_key=True)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
	teacher = db.relationship('Teacher', back_populates='timeslots')
	weekday = db.Column(db.String)
	time = db.Column(db.Time)
	bookings = db.relationship('Booking', back_populates='timeslots')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)


class Goal(db.Model):
	__tablename__ = 'goals'
	id = db.Column(db.Integer, primary_key=True)
	goal_slug = db.Column(db.String, unique=True)
	goal_text = db.Column(db.String, unique=True)
	teacher = db.relationship(
		'Teacher', secondary=teacher_goals_association, back_populates='goals')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)


class Student(db.Model):
	__tablename__ = 'students'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String, nullable=True, unique=True)
	phone = db.Column(db.String, unique=True)
	bookings = db.relationship('Booking', back_populates='student')
	requests = db.relationship('Request', back_populates='student')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)


class Request(db.Model):
	__tablename__ = 'requests'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	student = db.relationship('Student', back_populates='requests')
	goal = db.Column(db.String)
	have_time = db.Column(db.String)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)


class Booking(db.Model):
	__tablename__ = 'bookings'
	id = db.Column(db.Integer, primary_key=True)
	student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
	student = db.relationship('Student', back_populates='bookings')
	teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
	teacher = db.relationship('Teacher', back_populates='bookings')
	timeslot_id = db.Column(db.Integer, db.ForeignKey('timeslots.id'))
	timeslots = db.relationship('Timeslot', back_populates='bookings')
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(),  nullable=False)


db = SQLAlchemy()
