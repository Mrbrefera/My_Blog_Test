import pytest
from django.db import IntegrityError
from django.utils import timezone
from website.models import SiteInfo, SocialCount, Newsletter
from oeuvre.models import Poesie
from elenizado.models import Commentaire,Categorie, Publication, Like, Evenement, Video, ReponseCommentaire, Cours, Textes
from about.models import Contact, Curriculum, Prestation, Presentation, Gallerie

@pytest.mark.django_db
def test_curriculum_creation():
    # Test creation of Curriculum
    curriculum = Curriculum.objects.create(
        nom="Curriculum Test",
        description="Description of the curriculum",
        cv="path/to/cv",
    )
    assert curriculum.nom == "Curriculum Test"
    assert curriculum.description == "Description of the curriculum"
    assert curriculum.cv.name == "path/to/cv"
    assert curriculum.status is True
    assert str(curriculum) == "Curriculum Test"


@pytest.mark.django_db
def test_contact_creation():
    # Test creation of Contact
    contact = Contact.objects.create(
        nom="John Doe",
        email="john@example.com",
        subject="Inquiry",
        message="This is a test message."
    )
    assert contact.nom == "John Doe"
    assert contact.email == "john@example.com"
    assert contact.subject == "Inquiry"
    assert contact.message == "This is a test message."
    assert str(contact) == "John Doe"


@pytest.mark.django_db
def test_prestation_creation():
    # Test creation of Prestation
    prestation = Prestation.objects.create(
        titre="Prestation Title",
        description="Description of the prestation"
    )
    assert prestation.titre == "Prestation Title"
    assert prestation.description == "Description of the prestation"
    assert prestation.status is True
    assert str(prestation) == "Prestation Title"


@pytest.mark.django_db
def test_presentation_creation():
    # Test creation of Presentation
    presentation = Presentation.objects.create(
        titre="Presentation Title",
        description="Description of the presentation"
    )
    assert presentation.titre == "Presentation Title"
    assert presentation.description == "Description of the presentation"
    assert presentation.status is True
    assert str(presentation) == "Presentation Title"


@pytest.mark.django_db
def test_gallerie_creation():
    # Test creation of Gallerie
    gallerie = Gallerie.objects.create(
        titre="Gallery Title"
    )
    assert gallerie.titre == "Gallery Title"
    assert gallerie.status is True
    assert str(gallerie) == "Gallery Title"


@pytest.mark.django_db
def test_categorie_creation():
    # Test creation of Categorie
    categorie = Categorie.objects.create(
        nom="Category Name",
        description="Category description"
    )
    assert categorie.nom == "Category Name"
    assert categorie.description == "Category description"
    assert categorie.status is True
    assert str(categorie) == "Category Name"


@pytest.mark.django_db
def test_publication_creation():
    # Test creation of Publication
    categorie = Categorie.objects.create(
        nom="Category Name",
        description="Category description"
    )
    publication = Publication.objects.create(
        titre="Publication Title",
        description="Description of the publication",
        categorie=categorie
    )
    assert publication.titre == "Publication Title"
    assert publication.description == "Description of the publication"
    assert publication.categorie == categorie
    assert publication.status is True
    assert str(publication) == "Publication Title"


@pytest.mark.django_db
def test_commentaire_creation():
    # Test creation of Commentaire
    publication = Publication.objects.create(
        titre="Publication Title",
        description="Description of the publication"
    )
    commentaire = Commentaire.objects.create(
        publication=publication,
        nom="John Doe",
        commentaire="This is a test comment."
    )
    assert commentaire.nom == "John Doe"
    assert commentaire.commentaire == "This is a test comment."
    assert commentaire.publication == publication
    assert commentaire.status is True
    assert str(commentaire) == "John Doe"


@pytest.mark.django_db
def test_reponse_commentaire_creation():
    # Test creation of ReponseCommentaire
    commentaire = Commentaire.objects.create(
        nom="John Doe",
        commentaire="This is a test comment."
    )
    reponse = ReponseCommentaire.objects.create(
        commentaire=commentaire,
        nom="Jane Doe",
        reponse="This is a test reply."
    )
    assert reponse.nom == "Jane Doe"
    assert reponse.reponse == "This is a test reply."
    assert reponse.commentaire == commentaire
    assert reponse.status is True
    assert str(reponse) == "Jane Doe"


@pytest.mark.django_db
def test_like_creation():
    # Test creation of Like
    publication = Publication.objects.create(
        titre="Publication Title",
        description="Description of the publication"
    )
    like = Like.objects.create(
        publication=publication
    )
    assert like.publication == publication
    assert like.status is True
    assert str(like) == "Publication Title"


@pytest.mark.django_db
def test_evenement_creation():
    # Test creation of Evenement
    evenement = Evenement.objects.create(
        titre="Event Title",
        description="Description of the event"
    )
    assert evenement.titre == "Event Title"
    assert evenement.description == "Description of the event"
    assert evenement.status is True
    assert str(evenement) == "Event Title"


@pytest.mark.django_db
def test_cours_creation():
    # Test creation of Cours
    cours = Cours.objects.create(
        titre="Course Title",
        niveau="Beginner",
        annee=2024,
        description="Course description"
    )
    assert cours.titre == "Course Title"
    assert cours.niveau == "Beginner"
    assert cours.annee == 2024
    assert cours.description == "Course description"
    assert cours.status is True
    assert str(cours) == "Course Title"


@pytest.mark.django_db
def test_textes_creation():
    # Test creation of Textes
    texte = Textes.objects.create(
        titre="Text Title",
        description="Text description"
    )
    assert texte.titre == "Text Title"
    assert texte.description == "Text description"
    assert texte.status is True
    assert str(texte) == "Text Title"


@pytest.mark.django_db
def test_video_creation():
    # Test creation of Video
    video = Video.objects.create(
        titre="Video Title",
        description="Video description",
        video="http://youtube.com/example"
    )
    assert video.titre == "Video Title"
    assert video.description == "Video description"
    assert video.video == "http://youtube.com/example"
    assert video.status is True
    assert str(video) == "Video Title"


@pytest.mark.django_db
def test_poesie_creation():
    # Test creation of Poesie
    poesie = Poesie.objects.create(
        titre="Poem Title",
        description="Poem description",
        poeme="This is a test poem."
    )
    assert poesie.titre == "Poem Title"
    assert poesie.description == "Poem description"
    assert poesie.poeme == "This is a test poem."
    assert poesie.status is True
    assert str(poesie) == "Poem Title"


@pytest.mark.django_db
def test_siteinfo_creation():
    # Test creation of SiteInfo
    site_info = SiteInfo.objects.create(
        email="info@example.com",
        nom="My Site",
        telephone=123456789,
        description="Site description"
    )
    assert site_info.email == "info@example.com"
    assert site_info.nom == "My Site"
    assert site_info.telephone == 123456789
    assert site_info.description == "Site description"
    assert site_info.status is True
    assert str(site_info) == "My Site"


@pytest.mark.django_db
def test_socialcount_creation():
    # Test creation of SocialCount
    social_count = SocialCount.objects.create(
        nom="Facebook",
        lien="http://facebook.com",
        icones="fa-facebook-f"
    )
    assert social_count.nom == "Facebook"
    assert social_count.lien == "http://facebook.com"
    assert social_count.icones == "fa-facebook-f"
    assert social_count.status is True
    assert str(social_count) == "Facebook"


@pytest.mark.django_db
def test_newsletter_creation():
    # Test creation of Newsletter
    newsletter = Newsletter.objects.create(
        email="subscriber@example.com"
    )
    assert newsletter.email == "subscriber@example.com"
    assert newsletter.status is True
    assert str(newsletter) == "subscriber@example.com"

