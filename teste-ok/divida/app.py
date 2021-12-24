from flask import Flask, jsonify
from flask_restful import Api
from controller.dividaController import DividaRegister, Dividas, Divida
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

#rotas dividas
api.add_resource(Dividas, '/dividas')
api.add_resource(Divida, '/dividas/<string:divida_id>')
api.add_resource(DividaRegister, '/dividas/cadastro')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)