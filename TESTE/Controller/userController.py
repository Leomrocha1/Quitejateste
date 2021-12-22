from flask_restful import Resource, reqparse
from Model.userModel import UserModel
from validador_cpf import cpf_valido
from validador_data import data_valida
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('nome', type=str, required=True)
atributos.add_argument('cpf')
atributos.add_argument('data_nasc')

class Users(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário não existe'}, 404
    
    @jwt_required()
    def put(self, user_id):
        dados = atributos.parse_args()
        
        user_encontrado = UserModel.find_user(user_id)
        if user_encontrado:
            user_encontrado.update_user(**dados)
            user_encontrado.save_user()
            return user_encontrado.json(), 200
        return {'message': 'Usuário não existe'}
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'Usuário deletado com sucesso!'}
        return {'message': 'Usuário não existe'}, 404
    
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        if cpf_valido(dados['cpf']):
            if data_valida(dados['data_nasc']):
                if UserModel.find_by_cpf(dados['cpf']):
                    return {"message": "O cpf: {}, já existe!".format(dados['cpf'])}, 400
                user = UserModel(**dados)
                user.save_user()
                return {'message': 'Usuário criado com sucesso!'}, 201
            return{'message': 'A data {} é invalida.'.format(dados['data_nasc'])}
        return {'message': 'O CPF {} é invalido.'.format(dados['cpf'])}
    
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        
        user = UserModel.find_by_name(dados['nome'])

        if user and safe_str_cmp(user.cpf, dados['cpf']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'O nome ou cpf está incorreto.'}, 401
