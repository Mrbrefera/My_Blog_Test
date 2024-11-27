from django.test import TestCase
from django.urls import reverse
from django.core import mail
from website.models import SiteInfo, SocialCount, Newsletter
from oeuvre.models import Poesie
from elenizado.models import Commentaire,Categorie, Publication, Like, Evenement, Video, ReponseCommentaire
from about.models import Contact, Curriculum, Prestation, Presentation
from website.models import SiteInfo as WebsiteSiteInfo
import json

class IntegrationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Configuration des objets pour les tests d'intégration
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
        cls.publication = Publication.objects.create(
            title="Test Publication",
            content="This is a test publication",
            status=True
        )
        cls.contact_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'tel': '0123456789',
            'messages': 'This is a test message.'
        }

    def test_about_page_integration(self):
        """Test de l'intégration de la page About"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about-us.html')
        self.assertIn('about', response.context)
        self.assertIn('site_info', response.context)

    def test_contact_form_submission(self):
        """Test d'intégration pour soumettre un formulaire de contact"""
        response = self.client.post(reverse('is_contact'), self.contact_data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        
        # Vérifier si un objet Contact a été créé
        contact = Contact.objects.first()
        self.assertEqual(contact.nom, self.contact_data['name'])
        self.assertEqual(contact.email, self.contact_data['email'])

    def test_invalid_contact_form_submission(self):
        """Test d'intégration pour soumettre un formulaire de contact avec un email invalide"""
        invalid_contact_data = self.contact_data.copy()
        invalid_contact_data['email'] = 'invalid-email'
        
        response = self.client.post(reverse('is_contact'), invalid_contact_data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], "email incorrect")
        
        # Vérifier qu'aucun objet Contact n'a été créé
        self.assertEqual(Contact.objects.count(), 0)

    def test_comment_submission_for_publication(self):
        """Test d'intégration pour soumettre un commentaire pour une publication"""
        data = {
            'id': self.publication.id,
            'nom': 'John Doe',
            'email': 'johndoe@example.com',
            'commentaire': 'This is a test comment.'
        }
        response = self.client.post(reverse('is_commentaire'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        
        # Vérifier que le commentaire a été enregistré
        commentaire = ReponseCommentaire.objects.first()
        self.assertEqual(commentaire.nom, data['nom'])
        self.assertEqual(commentaire.email, data['email'])
        self.assertEqual(commentaire.commentaire, data['commentaire'])

    def test_reply_to_comment(self):
        """Test d'intégration pour répondre à un commentaire"""
        commentaire = Commentaire.objects.create(
            publication=self.publication,
            nom="Jane Doe",
            email="janedoe@example.com",
            commentaire="This is a reply to the test comment."
        )
        data = {
            'id_commentaire': commentaire.id,
            'id': self.publication.id,
            'name': 'John Doe',
            'mail': 'johndoe@example.com',
            'reponsecommentaires': 'This is a test response.'
        }
        response = self.client.post(reverse('is_reponsescommentaires'), data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], "l'enregistrement a bien été effectué")
        
        # Vérifier que la réponse au commentaire a été enregistrée
        reponse = ReponseCommentaire.objects.first()
        self.assertEqual(reponse.nom, data['name'])
        self.assertEqual(reponse.email, data['mail'])
        self.assertEqual(reponse.reponse, data['reponsecommentaires'])

    def test_full_integration_workflow(self):
        """Test d'intégration complet de soumission d'un contact et d'un commentaire"""
        # Soumettre un formulaire de contact
        contact_response = self.client.post(reverse('is_contact'), self.contact_data)
        self.assertEqual(contact_response.status_code, 200)
        contact_response_data = json.loads(contact_response.content)
        self.assertTrue(contact_response_data['success'])

        # Soumettre un commentaire
        data = {
            'id': self.publication.id,
            'nom': 'John Doe',
            'email': 'johndoe@example.com',
            'commentaire': 'This is a test comment.'
        }
        comment_response = self.client.post(reverse('is_commentaire'), data)
        self.assertEqual(comment_response.status_code, 200)
        comment_response_data = json.loads(comment_response.content)
        self.assertTrue(comment_response_data['success'])

        # Vérifier que le commentaire est bien lié à la publication
        commentaire = ReponseCommentaire.objects.first()
        self.assertEqual(commentaire.publication, self.publication)

        # Vérifier l'email reçu pour le contact (si l'email est configuré)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Contact Form Submission")
        self.assertIn(self.contact_data['name'], email.body)

