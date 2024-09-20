from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Utilisateur(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nom: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                           unique=True)
    courriel: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                                unique=True)
    mot_pass_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    publications: so.WriteOnlyMapped['Publication'] = so.relationship(
        back_populates='auteur')

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.nom)


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
