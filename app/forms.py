from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired
import sqlalchemy as sa
from app import db
import email_validator
from app.modeles import Utilisateur


class FormulaireSession(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    mot_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    memoriser = BooleanField('Mémoriser')
    soumettre = SubmitField('Ouvrir Session')


class FormulaireInscription(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    courriel = StringField('Courriel', validators=[DataRequired(), Email()])
    mot_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    mot_passe2 = PasswordField(
        'Répéter mot de passe', validators=[DataRequired(), EqualTo('mot_passe')])
    submit = SubmitField('Inscrire')

    def valide_nom(self, nom):
        utilisateur = db.session.scalar(sa.select(Utilisateur).where(
            Utilisateur.nom == nom.data))
        if utilisateur is not None:
            raise ValidationError(
                "Veuillez utiliser un nom d'utilisateur différent")

    def validate_courriel(self, courriel):
        utilisateur = db.session.scalar(sa.select(Utilisateur).where(
            Utilisateur.courriel == courriel.data))
        if utilisateur is not None:
            raise ValidationError(
                'Veuillez utiliser une autre adresse courriel')
