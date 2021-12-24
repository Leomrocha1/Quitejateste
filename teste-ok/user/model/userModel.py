from sql_alchemy import banco
from datetime import datetime
import requests

def verifica_dividas():
    url = 'http://127.0.0.1:5000'
    resposta = requests.request('GET', url + '/dividas')
    return str(resposta.json())
    

class UserModel(banco.Model):
    __tablename__ = 'users'
 
    user_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    cpf = banco.Column(banco.String(11))
    data_nasc = banco.Column(banco.String(11))
    criadoEm = banco.Column(banco.DateTime, default=datetime.now)
    data_att = banco.Column(banco.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, nome, cpf, data_nasc):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        
        
    def json(self):
        return {
            'user_id': self.user_id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nasc': self.data_nasc,
            'criadoEm': str(self.criadoEm),
            'data_att': str(self.data_att),
            'dividas': str(verifica_dividas())
        }


    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_cpf(cls, cpf):
        user_cpf = cls.query.filter_by(cpf=cpf).first()
        if user_cpf:
            return user_cpf
        return None
    
    @classmethod
    def find_by_name(cls, nome):
        user_name = cls.query.filter_by(nome=nome).first()
        if user_name:
            return user_name
        return None
    
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def update_user(self, nome, cpf, data_nasc):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
