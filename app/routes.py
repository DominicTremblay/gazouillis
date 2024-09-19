from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import FormulaireSession


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', titre='Home', user=user, posts=posts)


@app.route('/session', methods=['GET', 'POST'])
def ouvrir_session():
    form = FormulaireSession()
    if form.validate_on_submit():
        flash('Ouverture de session demander par {}, memoriser={}'.format(
            form.utilisateur.data, form.memoriser.data))
        return redirect(url_for('index'))
    return render_template('session.html', title='Ouverture Session', form=form)
