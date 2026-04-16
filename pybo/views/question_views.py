import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app
from werkzeug.utils import secure_filename

from pybo import db
from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer, User
from pybo.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', default=1, type=int)  # 페이지 쿼리 스트링값 가져오기
    kw = request.args.get('kw', default='', type=str)  # 검색 키워드 쿼리 스트링값 가져오기
    question_list = Question.query.order_by(Question.create_date.desc())

    if kw:
        search = f'%{kw}%'   # '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User)\
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
            .filter(
                Question.subject.ilike(search) |    # 질문 제목
                Question.content.ilike(search) |    # 질문 내용
                User.username.ilike(search) |       # 질문 작성자
                sub_query.c.content.ilike(search) | # 답변 내용
                sub_query.c.username.ilike(search)  # 답변 작성자
            ).distinct()

    question_list = question_list.paginate(page=page, per_page=10)  # 한 페이지에 보여야할 개수
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 폼에 전송된 이미지 파일 가져오기
        image_files = form.image.data
        image_paths = []

        # 저장 경로 : 오늘 날짜로 폴더 설정
        today = datetime.now().strftime('%Y%m%d')
        upload_folder = os.path.join(current_app.root_path, 'static/photo', today)
        os.makedirs(upload_folder, exist_ok=True)

        if image_files:
            for image_file in image_files:
                # 파일이 실제로 비어있지 않은지 확인
                if image_file and image_file.filename != '':
                    filename = secure_filename(image_file.filename)
                    file_path = os.path.join(upload_folder, filename)
                    image_file.save(file_path)

                    # DB용 상대 경로 리스트에 추가
                    image_paths.append(f'photo/{today}/{filename}')
        # 여러 경로를 하나의 문자열로 합침 (예: "path1,path2")
        # DB의 image_path 컬럼이 여러 경로를 담을 수 있을 만큼 길어야 합니다.
        joined_image_paths = ",".join(image_paths) if image_paths else None

        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now(),
            user=g.user,
            image_path=joined_image_paths  # 이미지 경로들 저장
        )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>/', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
        return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))