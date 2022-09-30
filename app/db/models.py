# Importar las librerias
from flask import Flask, jsonify, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    # main data
    email = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(30), unique=True)
    password_hashed = db.Column(db.String(128), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hashed = password
        
    
    @property
    def password(self):
        raise AttributeError('Password is not readable')

    def check_password(self,password):
        return self.password_hashed == password
    
    def get_id(self):
        return (self.email)

    def __repr__(self) -> str:
        return f'e: {self.email} \tu: {self.username} \tg: {self.github}'

class Carrito(db.Model):
    __tablename__ = "carrito"
    id = db.Column(db.Integer(), primary_key=True)
    producto = db.Column(db.String(), nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.email'), nullable=True)

    usuario = db.relationship("Usuario", backref="carritos")    
    def __repr__(self):
        response = {}
        response['producto'] = self.producto
        response['usuario'] = self.id_usuario 
        response['cantidad'] = self.cantidad
        return response

#db.create_all() #Crea las tablas 
#Rutas de la pagina