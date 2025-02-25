from datetime import datetime
import os
from flask_seeder import Seeder, Faker, generator
from werkzeug.security import generate_password_hash
from app.modeles import Utilisateur, Publication
from app import db
import csv

# All seeders inherit from Seeder


class UserSeeder(Seeder):

    def empty_database(self):
        """Supprime tous les enregistrements des tables de la base de données."""
        db.session.execute(db.delete(Publication))
        db.session.execute(db.delete(Utilisateur))
        db.session.commit()

    def lire_fichier_csv(self,  nom_fichier):
        acces_fichier = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', nom_fichier))
       
        """Lit un fichier CSV et retourne une liste de dictionnaires."""
        data = []
        with open(acces_fichier, newline='', encoding='utf-8') as fichier:
            lecteur = csv.reader(fichier)
            for rangee in lecteur:
                data.append(rangee)
        return data

    def ajout_utilisateurs(self, donnees_utilisateurs):
        """Ajoute des utilisateurs à la base de données."""
        # utilisateurs = []
        for rangee in donnees_utilisateurs:
            mot_passe_hash = generate_password_hash(rangee[2].strip())
            utilisateur = Utilisateur(
                nom=rangee[0],
                courriel=rangee[1],
                mot_passe_hash=mot_passe_hash,
                apropos=rangee[3]
            )
            print(f"Ajout utilisateur: {utilisateur.nom}")
            db.session.add(utilisateur)
            # utilisateurs.append(utilisateur)
        # return utilisateurs

    def ajout_publications(self, donnees_publications):
        """Ajoute des publications à la base de données."""
        for rangee in donnees_publications:
            user_id = int(rangee[0])
            contenu = rangee[1]
            horodatage = datetime.strptime(
                rangee[2].strip(), '%Y-%m-%d %H:%M:%S.%f')

            publication = Publication(
                contenu=contenu,
                user_id=user_id,
                horodatage=horodatage
            )
            print(f"Ajout publication: {publication.contenu}")
            db.session.add(publication)


    # Methode run appelee par Flask-Seeder
    def run(self):

        self.empty_database()

        donnees_utilisateurs = self.lire_fichier_csv(
            'data/utilisateur.csv')

        donnees_publications = self.lire_fichier_csv(
            'data/publication.csv')

        self.ajout_utilisateurs(donnees_utilisateurs)

        self.ajout_publications(donnees_publications)

        self.db.session.commit()
