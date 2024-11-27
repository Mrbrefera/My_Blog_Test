from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from website.models import SiteInfo, SocialCount, Newsletter
from oeuvre.models import Poesie
from elenizado.models import Commentaire , Commentaire as ElenizadoCommentaire, Categorie, Publication, Like, Evenement, Video, ReponseCommentaire, Cours, Textes
from about.models import  Contact, Curriculum, Prestation, Presentation, Gallerie
from website.models import SiteInfo as WebsiteSiteInfo
from django.core import mail
import json

class ViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Création d'un objet SiteInfo pour chaque test
        cls.site_info = SiteInfo.objects.create(
            email="info@example.com",
            nom="Mon Site",
            telephone="0123456789",
            description="Description du site",
            logo="path/to/logo.png",
            status=True
        )
        cls.presentation = Presentation.objects.create(
            title="Présentation du Site",
            content="Le contenu de la présentation",
            status=True
        )
        WebsiteSiteInfo.objects.create(
            email="webinfo@example.com",
            nom="Site Web",
            telephone="0123456789",
            description="Description du site web",
            logo="path/to/logo.png",
            status=True
        )

    def test_about_view(self):
        # Tester la vue 'about'
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about-us.html')
        self.assertIn('about', response.context)
        self.assertIn('site_info', response.context)

    def test_contact_view(self):
        # Tester la vue 'contact'
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact.html')
        self.assertIn('site_info', response.context)

    def test_author_view(self):
        # Tester la vue 'author'
        response = self.client.get(reverse('author'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/author-posts-2.html')
        self.assertIn('curriculum', response.context)
        self.assertIn('site_info', response.context)

    def test_is_contact_view_valid_data(self):
        # Tester le formulaire de contact avec des données valides
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'tel': '0123456789',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        # Vérifier si un objet Contact a été créé
        # self.assertEqual(Contact.objects.count(), 1)

    def test_is_contact_view_invalid_email(self):
        # Tester le formulaire de contact avec un email invalide
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'tel': '0123456789',
            'messages': 'This is a test message.'
        }
        response = self.client.post(reverse('is_contact'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], "email incorrect")
        # self.assertEqual(Contact.objects.count(), 0)

    def test_is_commentaire_view_valid_data(self):
        # Tester le formulaire de commentaire avec des données valides
        publication = Publication.objects.create(
            title="Test Publication",
            content="This is a test publication",
            status=True
        )
        data = {
            'id': publication.id,
            'nom': 'John Doe',
            'email': 'johndoe@example.com',
            'commentaire': 'This is a test comment.'
        }
        response = self.client.post(reverse('is_commentaire'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        # Vérifier si un objet Commentaire a été créé
        self.assertEqual(Commentaire.objects.count(), 1)

    def test_is_commentaire_view_invalid_email(self):
        # Tester le formulaire de commentaire avec un email invalide
        publication = Publication.objects.create(
            title="Test Publication",
            content="This is a test publication",
            status=True
        )
        data = {
            'id': publication.id,
            'nom': 'John Doe',
            'email': 'invalid-email',
            'commentaire': 'This is a test comment.'
        }
        response = self.client.post(reverse('is_commentaire'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], "email incorrect")
        self.assertEqual(Commentaire.objects.count(), 0)

    def test_is_reponsescommentaires_view_valid_data(self):
        # Tester la réponse aux commentaires avec des données valides
        publication = Publication.objects.create(
            title="Test Publication",
            content="This is a test publication",
            status=True
        )
        commentaire = ElenizadoCommentaire.objects.create(
            publication=publication,
            nom="John Doe",
            email="johndoe@example.com",
            commentaire="This is a test comment."
        )
        data = {
            'id_commentaire': commentaire.id,
            'id': publication.id,
            'name': 'Jane Doe',
            'mail': 'janedoe@example.com',
            'reponsecommentaires': 'This is a test response.'
        }
        response = self.client.post(reverse('is_reponsescommentaires'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        # Vérifier si un objet ReponseCommentaire a été créé
        self.assertEqual(ReponseCommentaire.objects.count(), 1)

    def test_is_reponsescommentaires_view_invalid_email(self):
        # Tester la réponse aux commentaires avec un email invalide
        publication = Publication.objects.create(
            title="Test Publication",
            content="This is a test publication",
            status=True
        )
        commentaire = ElenizadoCommentaire.objects.create(
            publication=publication,
            nom="John Doe",
            email="johndoe@example.com",
            commentaire="This is a test comment."
        )
        data = {
            'id_commentaire': commentaire.id,
            'id': publication.id,
            'name': 'Jane Doe',
            'mail': 'invalid-email',
            'reponsecommentaires': 'This is a test response.'
        }
        response = self.client.post(reverse('is_reponsescommentaires'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], "email incorrect")
        self.assertEqual(ReponseCommentaire.objects.count(), 0)
