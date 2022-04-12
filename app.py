from flask import Flask, request
# JWT 사용을 위한 SECRET_KEY 정보가 들어있는 파일 임포트
from flask.json import jsonify
from http import HTTPStatus
from config import Config

from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.price_ml import ml_rf
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource,jwt_blacklist

app = Flask(__name__)

# 환경 변수 셋팅
app.config.from_object(Config)

# JWT 토큰 만들기
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header,jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blacklist

api = Api(app)

# 경로와 리소스를 연결한다.
#유저 경로 리소스
api.add_resource(UserRegisterResource, '/v1/user/register') #회원가입
api.add_resource(UserLoginResource, '/v1/user/login') #로그인
api.add_resource(UserLogoutResource, '/v1/user/logout') #로그아웃
api.add_resource(ml_rf, '/v1/user/regressor') #예측



if __name__ == '__main__' :
    app.run()