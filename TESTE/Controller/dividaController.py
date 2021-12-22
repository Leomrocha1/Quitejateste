from flask_restful import Resource, reqparse
from Model.dividaModel import DividaModel
from Model.userModel import UserModel
from validador_data import data_valida

atributos = reqparse.RequestParser()
atributos.add_argument('valor', type=int, required=True)
atributos.add_argument('produto', type=str, required=True)
atributos.add_argument('data_venc', type=str, required=True)
atributos.add_argument('devedor_id', type=int, required=True)

class Dividas(Resource):
    def get(self):
        return {'dividas': [divida.json() for divida in DividaModel.query.all()]}

class Divida(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('valor', type=int, required=True)
    atributos.add_argument('produto', type=str, required=True)
    atributos.add_argument('data_venc', type=str, required=True)
    atributos.add_argument('devedor_id', type=int, required=True)

    def get(self, divida_id):
        divida = DividaModel.find_divida(divida_id)
        if divida:
            return divida.json()
        return {'message': 'Divida não encontrada!'}, 404

    def put(self, divida_id):
        dados = Divida.atributos.parse_args()

        divida_encontrada = DividaModel.find_divida(divida_id)
        if divida_encontrada:
            if not UserModel.find_user(dados['devedor_id']):
                return {'message': 'A divida deve estar associada a um usuário valido.'}, 400
            divida_encontrada.update_divida(**dados)
            divida_encontrada.save_divida()
            return divida_encontrada.json(), 200
        return {'message': 'Divida não encontrada!'}

    def delete(self, divida_id):
        divida = DividaModel.find_divida(divida_id)
        if divida:
            divida.delete_divida()
            return {'message': 'Divida deletada com sucesso!'}
        return {'message': 'Divida não encontrada!'}, 404

class DividaRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        divida = DividaModel(**dados)
        if(data_valida(dados['data_venc'])):   
            if not UserModel.find_user(dados['devedor_id']):
                return {'message': 'A divida deve estar associada a um usuário valido'}, 400
            divida.save_divida()
            return {'message': 'Divida cadastrada com sucesso!'}, 201
        return{'message': 'A data {} é invalida.'.format(dados['data_nasc'])}
