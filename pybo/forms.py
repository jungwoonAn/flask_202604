from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed
from wtforms.fields.simple import StringField, TextAreaField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])
    image = MultipleFileField('이미지 업로드', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message='이미지 파일만 업로드 가능합니다.')])
    submit = SubmitField('등록하기')

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호확인은 필수 입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수 입력 항목입니다.'), Email()])
    # 주소 필드 추가
    zip_code = StringField('우편번호', validators=[DataRequired()])
    address = StringField('주소', validators=[DataRequired()])
    detail_address = StringField('상세주소', validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.')])