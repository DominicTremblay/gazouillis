from typing import Optional
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return db.session.get(Utilisateur, int(id))


abonnes = sa.Table(
    'abonnes',
    db.metadata,
    sa.Column('fan_id', sa.Integer, sa.ForeignKey('utilisateur.id'),
              primary_key=True),
    sa.Column('abonnement_id', sa.Integer, sa.ForeignKey('utilisateur.id'),
              primary_key=True)
)


class Utilisateur(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nom: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                           unique=True)
    courriel: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                                unique=True)
    mot_passe_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    apropos: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    apercu: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    publications: so.WriteOnlyMapped['Publication'] = so.relationship(
        back_populates='auteur')

    # Users that this user is following (subscriptions)
    abonnements = so.relationship(
        'Utilisateur',
        secondary=abonnes,
        primaryjoin=(abonnes.c.fan_id == id),
        secondaryjoin=(abonnes.c.abonnement_id == id),
        back_populates='abonnes',
        lazy='dynamic'
    )

    # Users that follow this user (followers)
    abonnes = so.relationship(
        'Utilisateur',
        secondary=abonnes,
        primaryjoin=(abonnes.c.abonnement_id == id),
        secondaryjoin=(abonnes.c.fan_id == id),
        back_populates='abonnements',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)

    def encode_mot_passe(self, mot_passe):
        self.mot_passe_hash = generate_password_hash(mot_passe)

    def valide_mot_passe(self, mot_passe):
        return check_password_hash(self.mot_passe_hash, mot_passe)

    def avatar(self, taille):
        digest = md5(self.courriel.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={taille}'

    def suivre(self, utilisateur):
        if not self.est_fan(utilisateur):
            self.abonnements.add(utilisateur)

    def desabonner(self, utilisateur):
        if self.est_fan(utilisateur):
            self.abonnements.remove(utilisateur)

    def est_fan(self, utilisateur):
        # query = self.suivre.select().where(Utilisateur.id == utilisateur.id)
        # return db.session.scalar(query) is not None
        return utilisateur in self.abonnements

    def nombre_abonnes(self):
        return self.abonnes.count()

    def nombre_abonnements(self):
        return self.abonnements.count()

    # Retrouver les publications des utilisateurs que l'utilisateur courant suit
    def publications_abonnements(self):
        Auteur = so.aliased(Utilisateur)
        Abonne = so.aliased(Utilisateur)

        return (
            sa.select(Publication)
            # Join on the author of the publication
            .join(Publication.auteur.of_type(Auteur))
            # Only include posts from users this user follows
            .where(Abonne.id == self.id)
            # Order by timestamp in descending order
            .order_by(Publication.horodatage.desc())
        )

        # return (
        #     sa.select(Publication)
        #     .join(Publication.auteur.of_type(Auteur))
        #     .join(Auteur.abonnes)  # Join on 'abonnes' to get followers
        #     # Assuming the current user is the one who is following others
        #     .where(Auteur.id == self.id)
        #     # Changed 'timestamp' to 'horodatage'
        #     .order_by(Publication.horodatage.desc())
        # )

    # Retrouver les publications des utilisateurs qui suivent l'utilisateur courant
    def publications_abonnes(self):
        Auteur = so.aliased(Utilisateur)
        Abonne = so.aliased(Utilisateur)

        return (
            sa.select(Publication)
            # Join on the author of the publication
            .join(Publication.auteur.of_type(Auteur))
            .join(Auteur.abonnes.of_type(Abonne))  # Join on the followers
            # Only include posts from users this user follows
            .where(Abonne.id == self.id)
            # Exclude the current user's own posts
            .where(Publication.user_id != self.id)
            # Order by timestamp in descending order
            .order_by(Publication.horodatage.desc())
        )


class Publication(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contenu: so.Mapped[str] = so.mapped_column(sa.String(140))
    horodatage: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('utilisateur.id'), index=True)  # Foreign key

    auteur: so.Mapped[Utilisateur] = so.relationship(
        back_populates='publications')

    def __repr__(self):
        return '<Publication {}>'.format(self.contenu)
