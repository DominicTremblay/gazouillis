from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.modeles import Utilisateur, Publication
from app.forms import FormulaireSession, FormulaireInscription, EditProfileForm, FormulaireVide, FormulairePublication
from urllib.parse import urlsplit
from datetime import datetime, timezone


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.apercu = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    requete = current_user.publications_abonnements()

    publications = db.paginate(
        requete, page=page,
        per_page=app.config['PUBLICATIONS_PAR_PAGE'],
        error_out=False)

    url_suivant = url_for(
        'index', page=publications.next_num) if publications.has_next else None

    url_precedent = url_for(
        'index', page=publications.prev_num) if publications.has_prev else None

    formulaire = FormulairePublication()
    if formulaire.validate_on_submit():
        publication = Publication(
            contenu=formulaire.publication.data, auteur=current_user)
        db.session.add(publication)
        db.session.commit()
        flash('Votre publication est maintenant publiée')
        return redirect(url_for('index'))

    return render_template('index.html',
                           titre='Home',
                           publications=publications.items,
                           formulaire=formulaire,
                           url_suivant=url_suivant,
                           url_precedent=url_precedent)


@app.route('/explorer')
@login_required
def explorer():
    page = request.args.get('page', 1, type=int)
    requete = sa.select(Publication).order_by(Publication.horodatage.desc())

    publications = db.paginate(
        requete, page=page,
        per_page=app.config['PUBLICATIONS_PAR_PAGE'],
        error_out=False)

    url_suivant = url_for(
        'explorer', page=publications.next_num) if publications.has_next else None

    url_precedent = url_for(
        'explorer', page=publications.prev_num) if publications.has_prev else None

    return render_template('index.html',
                           titre='Explorer',
                           publications=publications.items,
                           url_suivant=url_suivant,
                           url_precedent=url_precedent)


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
    page = request.args.get('page', 1, type=int)
    requete_utilisateur = sa.select(Utilisateur).where(
        Utilisateur.nom == nom_utilisateur)
    utilisateur = db.session.scalars(requete_utilisateur).first()

    requete_publications = utilisateur.publications.select().order_by(Publication.horodatage.desc())

    publications = db.paginate(
        requete_publications, page=page,
        per_page=app.config['PUBLICATIONS_PAR_PAGE'],
        error_out=False)

    url_suivant = url_for(
        'utilisateur', nom_utilisateur=utilisateur.nom, page=publications.next_num) if publications.has_next else None

    url_precedent = url_for(
        'utilisateur', nom_utilisateur=utilisateur.nom, page=publications.prev_num) if publications.has_prev else None

    form = FormulaireVide()
    return render_template('profile.html',
                           utilisateur=utilisateur,
                           publications=publications,
                           form=form,
                           url_suivant=url_suivant,
                           url_precedent=url_precedent)


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


@app.route('/suivre/<nom_utilisateur>', methods=['POST'])
@login_required
def suivre(nom_utilisateur):
    form = FormulaireVide()
    if form.validate_on_submit():
        utilisateur = db.session.scalar(
            sa.select(Utilisateur).where(Utilisateur.nom == nom_utilisateur))
        if utilisateur is None:
            flash(f'Utilisateur {nom_utilisateur} introuvable.')
            return redirect(url_for('index'))
        if utilisateur == current_user:
            flash('Vous ne pouvez suivre vous memes')
            return redirect(url_for('utilisateur', nom_utilisateur=nom_utilisateur))
        current_user.suivre(utilisateur)
        db.session.commit()
        flash(f'Vous suivez {nom_utilisateur}!')
        return redirect(url_for('utilisateur', nom_utilisateur=nom_utilisateur))
    else:
        return redirect(url_for('index'))


@app.route('/desabonner/<nom_utilisateur>', methods=['POST'])
@login_required
def desabonner(nom_utilisateur):
    form = FormulaireVide()
    if form.validate_on_submit():
        utilisateur = db.session.scalar(
            sa.select(Utilisateur).where(Utilisateur.nom == nom_utilisateur))
        if utilisateur is None:
            flash(f'Utilisateur {nom_utilisateur} introuvable.')
            return redirect(url_for('index'))
        if utilisateur == current_user:
            flash('Vous ne pouvez vous desabonner de vous memes')
            return redirect(url_for('user', nom_utilisateur=nom_utilisateur))
        current_user.desabonner(utilisateur)
        db.session.commit()
        flash(f'Vous suivez plus {nom_utilisateur}!')
        return redirect(url_for('utilisateur', nom_utilisateur=nom_utilisateur))
    else:
        return redirect(url_for('index'))
