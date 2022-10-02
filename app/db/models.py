# Importar las librerias
from enum import unique
from flask import Flask, jsonify, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from .database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    email = db.Column(db.String(50), primary_key = True)
    username = db.Column(db.String(50), unique=True)
    password_hashed = db.Column(db.String(120), nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hashed = password
        
    
    @property    
    def check_password(self,password):
        return self.password_hashed == password
    
    def get_id(self):
        return (self.email)


class Pizzas(db.Model):
    __tablename__= "pizzas"
    
    name = db.Column(db.String(20),primary_key =True)
    size = db.Column(db.String(20),nullable=False)
    price = db.Column(db.Integer(),nullable = False)
    


    def __init__(self, name, size,price):
       
        self.name = name
        self.size = size
        self.price =price
        

    def __repr__(self):
        response = {}
        response['name'] = self.name
        response['size'] = self.size
        response['price'] = self.price
        
        return response
    
    

class Carrito(db.Model):
    __tablename__ = "carrito"
    id = db.Column(db.Integer(), primary_key=True)
    id_usuario = db.Column(db.String(50), db.ForeignKey('usuario.email'), nullable=False)
    producto = db.Column(db.String(20), db.ForeignKey('pizzas.name'), nullable=False)
  #  price = db.Column(db.Integer(), db.ForeignKey('pizzas.price'), nullable=False)
    cantidad = db.Column(db.Integer, nullable = False)   
    
    usuario = db.relationship("Usuario", backref="carrito")  
    pizzas = db.relationship("Pizzas", backref="carrito") 

    def __repr__(self):
        response = {}
        response['pizza'] = self.pizza
        response['usuario'] = self.id_usuario 
        response['price'] = self.price
        response['cantidad'] = self.cantidad
        
        return response




