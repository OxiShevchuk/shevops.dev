from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User
from extensions import db

