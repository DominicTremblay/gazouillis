from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import DataRequired
from wtforms import TextAreaField
from wtforms.validators import Length
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


class EditProfileForm(FlaskForm):
    nom = StringField("Nom d'utilisateur", validators=[DataRequired()])
    apropos = TextAreaField('A Propos', validators=[Length(min=0, max=140)])
    submit = SubmitField('Soumettre')

    def __init__(self, nom_origine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nom_origine = nom_origine

    def validate_username(self, nom):
        if nom.data != self.nom_origine:
            utilisateur = db.session.scalar(sa.select(Utilisateur).where(
                Utilisateur.nom == nom.data))
            if utilisateur is not None:
                raise ValidationError(
                    "Veuillez utiliser un nom d'utilisateur differend")


class FormulaireVide(FlaskForm):
    submit = SubmitField('Soumettre')


class FormulairePublication(FlaskForm):
    publication = TextAreaField('Dites quelquechose', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Soumettre')
