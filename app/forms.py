from flask import Blueprint, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    PasswordField,
    validators,
    FileField,
    Form,
    SubmitField
)


class LoginF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message = 'Espacio requerido'),
                 validators.length(min = 5, max = 30, message='No es valido')
                ])
    password =  PasswordField(
                 'Password',
                 [validators.DataRequired(message = 'Espacio requerido')]
                )
    
    def __init__(self, *args, **kwargs):
        super(LoginF, self).__init__(*args, **kwargs)

class SignUpF(Form):
    username = StringField(
                'Username',
                [validators.DataRequired(message = 'Espacio requerido'),
                 validators.length(min = 5, max = 30, message='No es valido')
                ])
    email = StringField(
                        'Email',
                        [validators.DataRequired(message= 'Debes colocar un correo')]
                        )
    password =  PasswordField(
                 'Password',
                 [validators.DataRequired(message = 'Espacio requerido')]
                )
              
    def __init__(self, *args, **kwargs):
        super(SignUpF, self).__init__(*args, **kwargs)

class ProductList(Form):

    producto = StringField(
                'Producto',
                [validators.DataRequired(message= 'Selecciona una pizza')]
                )
    cantidad =  StringField(
                 'Cantidad',
                 [validators.DataRequired(message = 'Debes seccionar una cantidad')]
                )
    size = StringField(
                 'Tamaño',
                 [validators.DataRequired(message = 'Espacio requerido')]
                )

    def __init__(self, *args, **kwargs):
        super(ProductList, self).__init__(*args, **kwargs)
