import json
import data
from models import *


def convert_data_to_json():
	teachers = data.teachers
	with open("teachers.json", "w", encoding='utf8') as f:
		json.dump(teachers, f, ensure_ascii=False)

	goals = data.goals
	with open("goals.json", "w", encoding='utf8') as f:
		json.dump(goals, f, ensure_ascii=False)



def get_teachers_from_json():
	with open("teachers.json", "r") as f:
		teachers = json.load(f)
	return teachers


def get_goals_from_json():
	with open("goals.json", "r") as f:
		goals = json.load(f)
	return goals


def json_teachers_to_db():
	teachers = get_teachers_from_json()

	for teacher in teachers:
		teacher_db = Teacher(
			name=teacher['name'],
			about=teacher['about'],
			rating=teacher['rating'],
			picture=teacher['picture'],
			price=teacher['price'],
			)
		db.session.add(teacher_db)

	db.session.commit()


def json_timeslots_to_db():
	teachers = get_teachers_from_json()

	for teacher in teachers:
		teacher_db = db.session.query(Teacher).filter(Teacher.name == teacher['name']).first()
		for weekday, time in teacher['free'].items():
			for t, v in time.items():
				if v:
					timeslots = Timeslot(teacher_id=teacher_db.id, weekday=weekday, time=t)
					db.session.add(timeslots)

	db.session.commit()


def json_goals_to_db():
	goals = get_goals_from_json()

	for goal in goals.items():
		goal_db = Goal(
			goal_slug=goal[0],
			goal_text=goal[1]
		)
		db.session.add(goal_db)
	db.session.commit()


def json_teachers_goals_to_db():
	teachers = get_teachers_from_json()

	for teacher in teachers:
		teacher_db = db.session.query(Teacher).filter(Teacher.name == teacher['name']).first()
		for goal in teacher['goals']:
			goal_db = db.session.query(Goal).filter(Goal.goal_slug == goal).first()
			teacher_db.goals.append(goal_db)
		db.session.commit()