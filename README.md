# Projet 11 - Améliorez une application Web Python par des tests et du débogage


## Güdlft
Güdlft est une plateforme numérique destinée à coordonner des compétitions. Ce projet a pour but de créer une version plus légère de la plateforme actuelle pour les organisateurs régionaux, permettant de rationaliser la gestion des compétitions entre les clubs.

## Table des Matières

- [Mise en Place et Installation](#mise-en-place-et-installation)
- [Fonctionnalités](#fonctionnalités)
- [Rapports de Tests](#rapports-de-tests)

## Mise en Place et Installation

### Prérequis

- Python 3.X
- Virtualenv
- Pip

### Installation

1. Clonez le dépôt Git sur votre machine locale :

    ```bash
    git clone git@github.com:El-GuiGui/P11-Ameliorez-une-application-Web-Python-par-des-tests-et-du-debogage-OP.git
    ```

    ```bash
    cd P11-Ameliorez-une-application-Web-Python-par-des-tests-et-du-debogage-OP
    ```

2. Créez un environnement virtuel :

    ```bash
    python -m venv env
    ```

3. Activez l'environnement virtuel :

      ```powershell
      env\Scripts\activate
      ```

4. Installez les dépendances définies dans le `requirements.txt` :

    ```bash
    pip install -r requirements.txt
    ```

5. Définissez la variable d'environnement Flask :

    ```bash
    set FLASK_APP=server.py
    ```

6. Lancez l'application Flask :

    ```bash
    flask --app server.py run
    ```

7. Accédez à l'application via votre navigateur à l'adresse suivante : `http://127.0.0.1:5000/`

## Fonctionnalités

- **Gestion des Compétitions **

- **Gestion des Utilisateurs **

- **Tableau des Points **

## Rapports de Tests

1. **Tests Unitaires et d'Intégration :**
   - Utilisez `pytest` pour exécuter les tests :

     ```bash
     pytest
     ```

   - Vérifiez la couverture de code avec `coverage` :

     ```bash
     coverage run -m pytest
     coverage report
     ```

2. **Tests de Performance :**
   - Utilisez `Locust` pour tester les performances :

     ```bash
     locust -f locustfile.py
     ```

3. **Documentation des Tests :**
   - présent dans le dossier reports_test&performance

