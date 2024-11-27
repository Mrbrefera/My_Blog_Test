import pytest
from django.urls import reverse
from django.test import Client
from website.models import SiteInfo, SocialCount, Newsletter
from oeuvre.models import  Poesie
from elenizado.models import Commentaire,Categorie, Publication
from about.models import Contact, Curriculum, Prestation, Presentation



@pytest.mark.django_db
def test_create_publication():
    # Test de la création d'une publication via une vue
    categorie = Categorie.objects.create(
        nom="Category A",
        description="Category description"
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Données de la publication à envoyer
    data = {
        'titre': "Test Publication",
        'description': "Description of the test publication",
        'categorie': categorie.id
    }

    # Envoi de la requête POST pour créer la publication
    response = client.post(reverse('publication_create'), data)

    # Vérifier que la publication a été créée et redirigée
    assert response.status_code == 302  # Redirection après succès (ex : vers la liste des publications)
    assert Publication.objects.count() == 1
    assert Publication.objects.first().titre == "Test Publication"
    assert Publication.objects.first().categorie == categorie


@pytest.mark.django_db
def test_update_publication():
    # Test de mise à jour d'une publication via une vue
    categorie = Categorie.objects.create(
        nom="Category A",
        description="Category description"
    )
    
    publication = Publication.objects.create(
        titre="Original Title",
        description="Original description",
        categorie=categorie
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Données mises à jour
    data = {
        'titre': "Updated Title",
        'description': "Updated description",
        'categorie': categorie.id
    }

    # Envoi de la requête POST pour mettre à jour la publication
    response = client.post(reverse('publication_update', kwargs={'pk': publication.id}), data)

    # Vérifier que la publication a été mise à jour et redirigée
    assert response.status_code == 302  # Redirection après succès (ex : vers la page de la publication)
    publication.refresh_from_db()
    assert publication.titre == "Updated Title"
    assert publication.description == "Updated description"


@pytest.mark.django_db
def test_delete_publication():
    # Test de la suppression d'une publication via une vue
    categorie = Categorie.objects.create(
        nom="Category A",
        description="Category description"
    )
    
    publication = Publication.objects.create(
        titre="Test Publication to Delete",
        description="Description for delete test",
        categorie=categorie
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Envoi de la requête POST pour supprimer la publication
    response = client.post(reverse('publication_delete', kwargs={'pk': publication.id}))

    # Vérifier que la publication a été supprimée
    assert response.status_code == 302  # Redirection après succès
    assert Publication.objects.count() == 0


@pytest.mark.django_db
def test_create_commentaire_for_publication():
    # Test de création d'un commentaire pour une publication
    publication = Publication.objects.create(
        titre="Test Publication for Comment",
        description="This publication is for testing comments"
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Données du commentaire
    data = {
        'nom': "Commenter 1",
        'commentaire': "This is a test comment",
        'publication': publication.id
    }

    # Envoi de la requête POST pour créer le commentaire
    response = client.post(reverse('commentaire_create'), data)

    # Vérifier que le commentaire a bien été créé
    assert response.status_code == 302  # Redirection après succès
    assert Commentaire.objects.count() == 1
    assert Commentaire.objects.first().nom == "Commenter 1"
    assert Commentaire.objects.first().commentaire == "This is a test comment"
    assert Commentaire.objects.first().publication == publication


@pytest.mark.django_db
def test_newsletter_subscription():
    # Test d'abonnement à la newsletter
    client = Client()

    # Données de l'abonnement à la newsletter
    data = {
        'email': "subscriber@example.com"
    }

    # Envoi de la requête POST pour s'abonner à la newsletter
    response = client.post(reverse('newsletter_subscribe'), data)

    # Vérifier que l'abonnement a été créé
    assert response.status_code == 302  # Redirection après succès
    assert Newsletter.objects.count() == 1
    assert Newsletter.objects.first().email == "subscriber@example.com"


@pytest.mark.django_db
def test_siteinfo_display():
    # Test de l'affichage des informations du site
    site_info = SiteInfo.objects.create(
        email="siteinfo@example.com",
        nom="My Site Info",
        telephone=987654321,
        description="Description of the site",
        logo="path/to/logo"
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Accéder à la page d'informations du site
    response = client.get(reverse('siteinfo_detail', kwargs={'pk': site_info.id}))

    # Vérifier que la page a été correctement affichée
    assert response.status_code == 200
    assert site_info.nom in response.content.decode()
    assert site_info.email in response.content.decode()


@pytest.mark.django_db
def test_create_and_view_poesie():
    # Test de la création et de l'affichage d'une poésie
    poesie = Poesie.objects.create(
        titre="Test Poem",
        description="This is a description of the poem",
        poeme="<p>This is the poem content</p>"
    )

    # Client pour effectuer des requêtes
    client = Client()

    # Accéder à la page de la poésie
    response = client.get(reverse('poesie_detail', kwargs={'pk': poesie.id}))

    # Vérifier que la page a été correctement affichée
    assert response.status_code == 200
    assert poesie.titre in response.content.decode()
    assert poesie.poeme in response.content.decode()
