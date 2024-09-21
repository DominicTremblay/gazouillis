from app.modeles import Utilisateur, Publication
from app import app, db
import unittest
from datetime import datetime, timezone, timedelta
import os
os.environ['DATABASE_URL'] = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Utilisateur(nom='susan', courriel='susan@example.com')
        u.encode_mot_passe('cat')
        self.assertFalse(u.valide_mot_passe('dog'))
        self.assertTrue(u.valide_mot_passe('cat'))

    def test_avatar(self):
        u = Utilisateur(nom='john', courriel='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        # Creer 2 utilisateurs
        u1 = Utilisateur(nom='john', courriel='john@example.com')
        u2 = Utilisateur(nom='susan', courriel='susan@example.com')

        # Ajouter les utilisateurs et commit a la base de donnees
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # On s'assure que personne n'est fan de l'autre
        self.assertFalse(u1.est_fan(u2))
        self.assertFalse(u2.est_fan(u1))

        # u1 n'a pas d'abonnement
        self.assertEqual(u1.nombre_abonnements(), 0)
        # u2 n'a pas d'abonnes
        self.assertEqual(u2.nombre_abonnes(), 0)

        # u1 suit u2
        u1.suivre(u2)
        db.session.commit()

        # Verifier que u1 est fan de u2
        self.assertTrue(u1.est_fan(u2))
        # u1 doit avoir 1 abonnement
        self.assertEqual(u1.nombre_abonnements(), 1)

        # Verifie si u2 possede 1 abonne
        # u1 doit etre dans les abonnes de u2
        self.assertEqual(u2.nombre_abonnes(), 1)
        self.assertIn(u1, u2.abonnes.all())

        # On s'assure que u2 n'est pas fan de u1
        self.assertFalse(u2.est_fan(u1))

        # u1 va suivre u2
        u1.suivre(u2)
        db.session.commit()

        # Vérification si u1 suit u2
        self.assertTrue(u1.est_fan(u2))
        self.assertEqual(u1.nombre_abonnements(), 1)
        self.assertEqual(u2.nombre_abonnes(), 1)

        # Utilisation de .all() pour récupérer les abonnements et les abonnés
        u1_abonnements = u1.abonnements.all()  # Utilisateur que u1 suit
        u2_abonnes = u2.abonnes.all()  # Utilisateur qui suit u2

        # Vérification des résultats
        self.assertEqual(u1_abonnements[0].nom, 'susan')  # u1 suit u2 (susan)
        self.assertEqual(u2_abonnes[0].nom, 'john')  # u2 a john comme abonné

        u1.desabonner(u2)
        db.session.commit()
        self.assertFalse(u1.est_fan(u2))
        self.assertEqual(u1.nombre_abonnements(), 0)
        self.assertEqual(u2.nombre_abonnes(), 0)

    def test_follow_posts(self):
        # Créer quatre utilisateurs
        u1 = Utilisateur(nom='john', courriel='john@example.com')
        u2 = Utilisateur(nom='susan', courriel='susan@example.com')
        u3 = Utilisateur(nom='mary', courriel='mary@example.com')
        u4 = Utilisateur(nom='david', courriel='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # Créer quatre publications
        now = datetime.now(timezone.utc)
        p1 = Publication(contenu="post from john", auteur=u1,
                         horodatage=now + timedelta(seconds=1))
        p2 = Publication(contenu="post from susan", auteur=u2,
                         horodatage=now + timedelta(seconds=4))
        p3 = Publication(contenu="post from mary", auteur=u3,
                         horodatage=now + timedelta(seconds=3))
        p4 = Publication(contenu="post from david", auteur=u4,
                         horodatage=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Configurer les abonnements (followers)
        u1.suivre(u2)  # john suit susan
        u1.suivre(u4)  # john suit david
        u2.suivre(u3)  # susan suit mary
        u3.suivre(u4)  # mary suit david
        db.session.commit()

        # Vérifier les publications des utilisateurs suivis pour chaque utilisateur
        # john voit les posts de ceux qu'il suit
        f1 = db.session.scalars(u1.publications_abonnes()).all()
        # susan voit les posts de ceux qu'elle suit
        f2 = db.session.scalars(u2.publications_abonnes()).all()
        # mary voit les posts de ceux qu'elle suit
        f3 = db.session.scalars(u3.publications_abonnes()).all()
        # david ne suit personne, il ne voit que ses propres posts
        f4 = db.session.scalars(u4.publications_abonnes()).all()

        # Vérifier que les posts récupérés sont bien ordonnés par horodatage décroissant
        self.assertEqual(f1, [p2, p4])  # john voit les posts de susan et david
        self.assertEqual(f2, [p3])  # susan voit uniquement le post de mary
        self.assertEqual(f3, [p4])  # mary voit uniquement le post de david
        # david ne suit personne donc pas de posts suivis
        self.assertEqual(f4, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
