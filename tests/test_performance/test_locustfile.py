from locust import HttpUser, task, between
import json

class WebsiteUser(HttpUser):
    # Temps de pause entre les tâches (en secondes)
    wait_time = between(1, 5)  # Un utilisateur attend entre 1 et 5 secondes avant de faire une nouvelle tâche.

    # Définit la tâche principale (exécution d'une série de requêtes HTTP)
    @task(1)  # La priorité de cette tâche est de 1 (par rapport aux autres tâches).
    def load_homepage(self):
        self.client.get("/")  # Effectue une requête GET sur la page d'accueil.

    @task(2)
    def load_about_page(self):
        self.client.get("/about")  # Effectue une requête GET sur la page "about".

    @task(3)
    def load_contact_page(self):
        self.client.get("/contact")  # Effectue une requête GET sur la page "contact".

    @task(1)
    def submit_newsletter(self):
        # Envoie une requête POST simulant l'inscription à une newsletter.
        self.client.post("/is_newsletter", json={"email": "testuser@example.com"})

    @task(1)
    def submit_contact_form(self):
        # Envoie une requête POST simulant l'envoi d'un formulaire de contact.
        self.client.post("/is_contact", json={
            "name": "John Doe",
            "email": "johndoe@example.com",
            "subject": "Test Subject",
            "tel": "1234567890",
            "messages": "This is a test message."
        })

    @task(1)
    def load_publications(self):
        # Effectue une requête GET sur la page des publications (en fonction de votre application).
        self.client.get("/timeline")

    @task(1)
    def load_event_details(self):
        # Effectue une requête GET sur une page d'événement avec un slug spécifique.
        self.client.get("/details_events/some-event-slug/")

    @task(1)
    def load_poetry_page(self):
        # Effectue une requête GET sur la page contenant les poésies.
        self.client.get("/poeme")
    
    @task(1)
    def load_video_page(self):
        # Effectue une requête GET sur la page des vidéos.
        self.client.get("/video")
    
    @task(1)
    def load_course_page(self):
        # Effectue une requête GET sur la page des cours.
        self.client.get("/cours")
