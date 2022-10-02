from distutils.errors import PreprocessError
from http import client
import json
from msilib import CAB
import os
from os import access, getenv
from unicodedata import name
from urllib import response
from flask import (
    Blueprint,
    Flask,
    flash,
    abort,
    jsonify,
    render_template, 
    redirect, 
    session, 
    url_for, 
    request
)
from flask_login import (
    LoginManager, 
    UserMixin, 
    login_user, 
    login_required,
    current_user
)
import hashlib
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from .db.database import db

from . import forms 
from .db.models import Carrito, Usuario, Pizzas
from werkzeug.utils import secure_filename

app = Blueprint('login', __name__, 
                template_folder='templates')  

def init_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_email):
        return Usuario.query.get(user_email)

@app.route('/', methods=['GET'])
def index():
    nombre1 =  Pizzas.query.filter_by(name = "Americana").first()
    if nombre1 is None:
        p1 = Pizzas(name = "Americana",size = "personal",price =10)
        db.session.add(p1)
        db.session.commit()

    
    p2 = Pizzas(name = "Peperoni",size = "personal",price =10)
    p3 = Pizzas(name = "Hawaiana",size = "personal",price =10)
    p4 = Pizzas(name = "Vegetariana",size = "personal",price =10)
    p5 = Pizzas(name = "Chicken BBQ",size = "personal",price =10)
    p6 = Pizzas(name = "Suprema",size = "personal",price =10)
    p7 = Pizzas(name = "Napolitana",size = "personal",price =10)
    p8 = Pizzas(name = "Margarita",size = "personal",price =10)
    p9 = Pizzas(name = "Meet Lover",size = "personal",price =10)
    p10 = Pizzas(name = "Champiñones",size = "personal",price =10)

    
    lista =[p2,p3,p4,p5,p6,p7,p8,p9,p10]
    for i in lista:
        verificar = i.name
        nombre =  Pizzas.query.filter_by(name = verificar).first()
        if nombre is None:
            db.session.add(i)
            db.session.commit()
    

    return render_template('Inicio.html')



@app.route('/sign-up/', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpF(request.form)
    if request.method == 'POST':
        nuevo_usuario = Usuario(form.email.data, 
                                form.username.data, 
                                form.password.data)       

        db.session.add(nuevo_usuario)
        db.session.commit()
        login_user(nuevo_usuario)

        return redirect(url_for('login.inicio'))
        
    elif request.method=='GET':                
        return render_template('signup.html', form = form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginF(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        usuario =  Usuario.query.filter_by(username = username).first()
        if (usuario is not None and 
            usuario.check_password(password)) : #Entra si el usuario existe, tiene correcta la contraseña y está confirmado
            
            login_user(usuario, remember=True)
            return redirect(url_for('login.inicio'))
        else: 
            print("No entraste :(")
        
        return render_template("login.html", form=form)
    else: 
        return render_template("login.html", form=form)

@app.route('/inicio',methods = ['GET', 'POST'])
@login_required
def inicio():
    form = forms.ProductList(request.form)
    if request.method == 'POST': 
        productlist = Carrito(
                    producto=form.producto.data,  
                    cantidad = form.cantidad.data,
                    id_usuario= current_user.email,
                )
        db.session.add(productlist)  
        db.session.commit()
        subquery = db.session.query(Carrito.id).filter(Carrito.id_usuario == current_user.email).subquery()
        p = Carrito.query.filter(Carrito.id.in_(subquery)).order_by('id').all()
    
        if p is not None:
            return redirect('inicio')
        
    subquery = db.session.query(Carrito.id).filter(Carrito.id_usuario == current_user.email).subquery()
    p = Carrito.query.filter(Carrito.id.in_(subquery)).order_by('id').all()   
    return render_template('index.html', form = form, cursos = p)

@app.route('/show-data/<user>', methods=['GET'])
@login_required
def agregar(user):
    response = {}
    id = int(user)
    todo = Carrito(id=id)
    carrito = Carrito.query.get(user)
    response['producto'] = carrito.producto
    response['cantidad'] = carrito.cantidad
    response['user'] = carrito.id_usuario
    return jsonify(response)

@app.route('/actualizar/<id>', methods=['GET','POST'])
@login_required
def actualizar(id):
    form = forms.ProductList(request.form)
    if request.method == 'POST':
        carrito = Carrito.query.filter(Carrito.id == id).one_or_none()
        Carrito.producto = form.producto.data
        Carrito.cantidad = int(form.cantidad.data)
        db.session.commit()
        return redirect(url_for('login.inicio'))
    return render_template('actualizar.html', form = form, id=id)

@app.route('/delete/<id>', methods=['DELETE'])
@login_required
def eliminar(id):
    response = {}
    try:
        carrito = Carrito.query.get(id) # 1 registro
        db.session.delete(carrito)
        response['id'] = carrito.id
        db.session.commit()
        return jsonify(response)
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify(response)
