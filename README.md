**APPLICATION ECRAN RASPBERRY** 

- Version: 1.0
- By Orange Academy
- Avec l'aide de [Hui Wen]( https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html) pour la base du calendrier


**Configuration**

1. Utiliser fichier de ecalendar.sql pour migrer les tables
2. Créer superuser pour administration
3. Ajouter les informations de la nouvelle salle (room) pour laquelle 
est utilisée l'application depuis l'administration de Djnago ou directement à la base de donnée


**Fonctionnalités**

1. Consulter Calendrier des évènements, navigation par mois
2. Ajouter un nouvel évènement (qui doit être confirmé sur l'application 
de réservation avent d'être affiché)
3. Aller vesr Administration


**API**

- **Constants**
    API_URL: 'http://localhost:8000/api/v1/'

- **Views**

    def get_context_data(self, **kwargs):
        Acquérir information nécessaire à l'affichage

    def prev_month(d):
        Retourne le mois précédent

    def next_month(d):
        Retourne le mois précédent

    def get_date(req_day):
        Retourne la date

    def event(request):
        Formatter données du nouvel évènement et envoie à l'APi de réservation
    
    def verify_ok(request, day, start, end):
        Vérifier que la salle est disponible pour nouvel évènement
    
    def get_events():
        Récupérer les divers évènements de l'API de réservation

- **Utils**

    def formatday(self, day, events):
        formatter l'affichage des jours du calendriers
    
    (Fonctionnement analogue pour les autres fonctions formatxx())

    def authenticate():
        S'authentifier après de l'API de réservation

- **Forms**

    def get_disposition():
        Récupérer les différentes dispositions de l'API


Mounya Kamidjigha
mkamidjigha@gmail.com
    





















