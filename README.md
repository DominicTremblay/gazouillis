# Tutoriel Gazoullis

## Chapitre 5 - Creer une session

- Algorithme de Hashing du mot de passe
  - methodes: `generate_password_hash`, `check_password_hash`

- Creation de la session
  - `flask-login`
  - Ajout de proprietes et mPethodes au modele `Utilisateur` avec `UserMixin`
  - Modification de la route `session` pour creer une session
  - Creer la route `deconnexion` pour detruire la session
  - Creer un menu conditionnel pour afficher les liens de connexion/deconnexion
  - Utilisation de `current_user.is_anonymous` dans `base.html` pour afficher le menu conditionnel
  - Requerir une connexion de l'utilisateur pour acceder a certaines routes `@login_required`
  - Enregistrement de l'utilisateur dans la session avec `login_user`

## Chapitre 6 - Page profile et avatars

- Creer la route pour le profile `/utilisateurs/<nom>`
- Ajouter les avatars aux utilisateurs (gravatars)
- Sous-templates pour les publications


