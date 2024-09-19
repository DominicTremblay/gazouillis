from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class FormulaireSession(FlaskForm):
    utilisateur = StringField('Username', validators=[DataRequired()])
    mot_passe = PasswordField('Password', validators=[DataRequired()])
    memoriser = BooleanField('Mémoriser')
    soumettre = SubmitField('Ouvrir Session')