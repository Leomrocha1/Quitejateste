from sql_alchemy import banco
from datetime import datetime

class DividaModel(banco.Model):
    __tablename__ = 'dividas'
    
    divida_id = banco.Column(banco.Integer, primary_key=True)
    valor = banco.Column(banco.Float(precision=2))
    produto = banco.Column(banco.String(100))
    data_venc = banco.Column(banco.String(11))
    devedor_id = banco.Column(banco.Integer, banco.ForeignKey('users.user_id'))
    users = banco.relationship('UserModel')
    criadoEm = banco.Column(banco.DateTime, default=datetime.now)
    data_att = banco.Column(banco.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __init__(self, valor, produto, devedor_id, data_venc):
        self.valor = valor
        self.produto = produto
        self.data_venc = data_venc
        self.devedor_id = devedor_id
   
    def json(self):
        return {
            'divida_id': self.divida_id,
            'valor': self.valor,
            'produto': self.produto,
            'data_venc': self.data_venc,
            'devedor_id': self.devedor_id,
            'criadoEm': str(self.criadoEm),
            'data_att': str(self.data_att)
        }

    @classmethod
    def find_divida(cls, divida_id):
        divida = cls.query.filter_by(divida_id=divida_id).first()
        if divida:
            return divida
        return None
    
    def save_divida(self):
        banco.session.add(self)
        banco.session.commit()

    def update_divida(self, valor, produto, data_venc, devedor_id):
        self.valor = valor
        self.produto = produto
        self.data_venc = data_venc
        self.user_id = devedor_id
    
    def delete_divida(self):
        banco.session.delete(self)
        banco.session.commit()
