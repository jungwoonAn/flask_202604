from flask import Flask

def create_app():  # 애플리케이션 팩토리
    app = Flask(__name__)

    # 블루프린트 등록
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app