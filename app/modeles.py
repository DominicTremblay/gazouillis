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

class Utilisateur(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nom: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                           unique=True)
    courriel: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                                unique=True)
    mot_passe_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    apropos: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    apercu: so.Mapped[Optional[datetime]] = so.mapped_column(default=lambda: datetime.noew(timezone.utc))

    publications: so.WriteOnlyMapped['Publication'] = so.relationship(
        back_populates='auteur')

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)
    
    def encode_mot_passe(self, mot_passe):
        self.mot_passe_hash = generate_password_hash(mot_passe)

    def valide_mot_passe(self, mot_passe):
        return check_password_hash(self.mot_passe_hash, mot_passe)
    
    def avatar(self, taille):
        digest = md5(self.courriel.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={taille}'

class Publication(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    contenu: so.Mapped[str] = so.mapped_column(sa.String(140))
    horodatage: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Utilisateur.id),
                                               index=True)

    auteur: so.Mapped[Utilisateur] = so.relationship(
        back_populates='publications')

    def __repr__(self):
        return '<Publication {}>'.format(self.contenu)



