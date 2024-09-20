from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.modeles import Utilisateur
from app.forms import FormulaireSession, FormulaireInscription, EditProfileForm
from urllib.parse import urlsplit
from datetime import datetime, timezone


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.apercu = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    publications = [
        {
            'auteur': {'utilisateur': 'John'},
            'contenu': 'Beautiful day in Portland!'
        },
        {
            'auteur': {'utilisateur': 'Susan'},
            'contenu': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', titre='Home', publications=publications)


@app.route('/session', methods=['GET', 'POST'])
def ouvrir_session():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formulaire = FormulaireSession()
    # This will list all attributes and methods of the form
    print(dir(formulaire))

    if formulaire.validate_on_submit():
        utilisateur = db.session.scalar(
            sa.select(Utilisateur).where(Utilisateur.nom == formulaire.nom.data))
        if utilisateur is None or not utilisateur.valide_mot_passe(formulaire.mot_passe.data):
            flash('Utilisateur ou mot de passe invalide')
            return redirect(url_for('ouvrir_session'))
        login_user(utilisateur, remember=formulaire.memoriser.data)
        page_suivante = request.args.get('next')
        if not page_suivante or urlsplit(page_suivante).netloc != '':
            page_suivante = url_for('index')
        return redirect(page_suivante)
    return render_template('session.html', titre='Ouverture Session', form=formulaire)


@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('index'))


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    formulaire = FormulaireInscription()
    if formulaire.validate_on_submit():
        utilisateur = Utilisateur(
            nom=formulaire.nom.data, courriel=formulaire.courriel.data)
        utilisateur.encode_mot_passe(formulaire.mot_passe.data)
        db.session.add(utilisateur)
        db.session.commit()
        flash('Vous êtes maintenant enregistré')
        return redirect(url_for('ouvrir_session'))
    return render_template('inscrire.html', title='Inscription', form=formulaire)


@app.route('/utilisateurs/<nom_utilisateur>')
@login_required
def utilisateur(nom_utilisateur):
    utilisateur = db.first_or_404(
        sa.select(Utilisateur).where(Utilisateur.nom == nom_utilisateur))
    publications = [
        {'auteur': utilisateur, 'contenu': 'Test #1'},
        {'auteur': utilisateur, 'contenu': 'Test #2'}
    ]
    return render_template('profile.html', utilisateur=utilisateur, publications=publications)


@app.route('/editer_profile', methods=['GET', 'POST'])
@login_required
def editer_profile():
    form = EditProfileForm(current_user.nom)
    if form.validate_on_submit():
        current_user.nom = form.nom.data
        current_user.apropos = form.apropos.data
        db.session.commit()
        flash("Vos changements ont été sauvegardés")
        return redirect(url_for('editer_profile'))
    elif request.method == 'GET':
        form.nom.data = current_user.nom
        form.apropos.data = current_user.apropos
    return render_template('editer_profile.html', titre="Editer profile", form=form)
