from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, RadioField
from wtforms.validators import Length, InputRequired


class BookingForm(FlaskForm):
    name = StringField("Ваше имя", [Length(min=1, max=25), InputRequired(message="Напишите своё имя")])
    phone = StringField("Ваш телефон", [Length(min=1, max=25), InputRequired(message="Напишите свой телефон")])
    day = HiddenField()
    time = HiddenField()
    teacher_id = HiddenField()
    timeslot_id = HiddenField()
    teacher_name = HiddenField()
    submit = SubmitField("Записаться на пробный урок")


class RequestForm(FlaskForm):
    name = StringField("Ваше имя", [Length(min=1, max=25), InputRequired(message="Напишите своё имя")])
    phone = StringField("Ваш телефон", [Length(min=1, max=25), InputRequired(message="Напишите свой телефон")])
    goal = RadioField('Какая цель занятий?', choices=[
        ('⛱ Для путешествий', '⛱ Для путешествий'),
        ('🏫 Для учебы', '🏫 Для учебы'),
        ('🏢 Для работы', '🏢 Для работы'),
        ('🚜 Для переезда', '🚜 Для переезда'),
        ('💻 Для программирования', '💻 Для программирования')
    ])
    have_hours = RadioField('Сколько времени есть?', choices=[
        ('1-2 часа в неделю', '1-2 часа в неделю'),
        ('3-5 часов в неделю', '3-5 часов в неделю'),
        ('5-7 часов в неделю', '5-7 часов в неделю'),
        ('7-10 часов в неделю', '7-10 часов в неделю')
    ])
    submit = SubmitField("Найдите мне преподавателя")
