import pytest
from django.db import IntegrityError
from django.utils import timezone
from website.models import SiteInfo, SocialCount, Newsletter
from oeuvre.models import Poesie
from elenizado.models import Commentaire,Categorie, Publication, Like, Evenement, Video
from about.models import Contact, Curriculum, Prestation, Presentation

@pytest.mark.django_db
def test_publication_creation_with_categorie():
    # Test de création d'une Publication avec une Categorie
    categorie = Categorie.objects.create(
        nom="Category A",
        description="Category description"
    )
    
    publication = Publication.objects.create(
        titre="Test Publication",
        description="This is a test description for the publication",
        categorie=categorie
    )

    # Vérifier que la publication a bien été associée à la catégorie
    assert publication.categorie == categorie
    assert publication.titre == "Test Publication"
    assert publication.description == "This is a test description for the publication"
    assert publication.status is True

    # Vérifier la relation inverse (Category -> Publications)
    assert categorie.categorie_publication.count() == 1
    assert categorie.categorie_publication.first() == publication


@pytest.mark.django_db
def test_commentaire_creation_and_association_to_publication():
    # Test de la création d'un commentaire et son association à une publication
    publication = Publication.objects.create(
        titre="Publication for Comment",
        description="This publication is for testing comments"
    )
    
    commentaire = Commentaire.objects.create(
        publication=publication,
        nom="Commenter 1",
        commentaire="This is a test comment"
    )

    # Vérification des données
    assert commentaire.publication == publication
    assert commentaire.nom == "Commenter 1"
    assert commentaire.commentaire == "This is a test comment"
    assert commentaire.status is True

    # Vérifier la relation inverse (Publication -> Commentaires)
    assert publication.publication_commentaire.count() == 1
    assert publication.publication_commentaire.first() == commentaire


@pytest.mark.django_db
def test_reponse_commentaire_creation_and_association():
    # Test de création d'une réponse à un commentaire
    publication = Publication.objects.create(
        titre="Publication for Reply",
        description="This publication is for testing replies"
    )
    
    commentaire = Commentaire.objects.create(
        publication=publication,
        nom="Commenter 2",
        commentaire="This is a test comment"
    )
    
    reponse = Commentaire.objects.create(
        commentaire=commentaire,
        nom="Replier 1",
        reponse="This is a test reply"
    )

    # Vérifier que la réponse est bien associée au commentaire
    assert reponse.commentaire == commentaire
    assert reponse.nom == "Replier 1"
    assert reponse.reponse == "This is a test reply"
    assert reponse.status is True

    # Vérifier la relation inverse (Commentaire -> Réponses)
    assert commentaire.reponse_commentaire.count() == 1
    assert commentaire.reponse_commentaire.first() == reponse


@pytest.mark.django_db
def test_like_association_to_publication():
    # Test de création d'un Like pour une publication
    publication = Publication.objects.create(
        titre="Publication for Like",
        description="This publication is for testing likes"
    )

    like = Like.objects.create(
        publication=publication
    )

    # Vérifier que le like est bien associé à la publication
    assert like.publication == publication
    assert like.status is True

    # Vérifier la relation inverse (Publication -> Likes)
    assert publication.like_publication.count() == 1
    assert publication.like_publication.first() == like


@pytest.mark.django_db
def test_evenement_creation_and_slug_generation():
    # Test de création d'un événement et génération automatique du slug
    evenement = Evenement.objects.create(
        titre="Event for Slug Test",
        description="Description for testing slug"
    )

    # Vérification du slug généré
    assert evenement.slug is not None
    assert evenement.slug == '-'.join(("event-for-slug-test", str(evenement.slug.split('-')[-1])))
    assert evenement.titre == "Event for Slug Test"
    assert evenement.description == "Description for testing slug"
    assert evenement.status is True


@pytest.mark.django_db
def test_siteinfo_and_social_count_integration():
    # Test de l'intégration de SiteInfo avec SocialCount
    site_info = SiteInfo.objects.create(
        email="siteinfo@example.com",
        nom="My Site Info",
        telephone=987654321,
        description="Description of the site",
        logo="path/to/logo"
    )

    # Création de comptes de réseaux sociaux associés
    social_facebook = SocialCount.objects.create(
        nom="Facebook",
        lien="http://facebook.com",
        icones="fa-facebook-f"
    )

    social_twitter = SocialCount.objects.create(
        nom="Twitter",
        lien="http://twitter.com",
        icones="fa-twitter"
    )

    # Vérification que les informations sont bien associées
    assert site_info.socialcount_set.count() == 2
    assert social_facebook.siteinfo_set.count() == 1
    assert social_twitter.siteinfo_set.count() == 1


@pytest.mark.django_db
def test_newsletter_subscription_and_status():
    # Test de l'intégration de la newsletter
    newsletter = Newsletter.objects.create(
        email="subscriber@example.com"
    )

    # Vérifier que l'email a bien été ajouté à la newsletter
    assert newsletter.email == "subscriber@example.com"
    assert newsletter.status is True


@pytest.mark.django_db
def test_video_url_property():
    # Test de la propriété `get_video` sur la vidéo
    video = Video.objects.create(
        titre="Video Title",
        description="Video description",
        video="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    # Vérifier la récupération de l'ID de la vidéo depuis l'URL
    video_id = video.get_video
    assert video_id == "dQw4w9WgXcQ"


