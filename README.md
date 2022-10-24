# Bundesliga Web App
A web app that communicates with the Bundesliga API - https://www.openligadb.de/

## How it works?
### The custom request handler fetches data from the API and provides the following information:
- Upcoming matches for the following day
- All matches of the current season
- Win/Loss Ratio information (Leaderboard)
- Manual search for each team's info such as - all matches for the current season; upcoming matches; win/loss ratio

### Features
- Minified HTML/CSS/JS code using "django-minify-html" (https://pypi.org/project/django-minify-html/)
- Responsive design for different devices using Bootstrap 


## How to set it up?
- Clone the repository
- Once you've cloned the inventory, navigate into it
- Create a virtual environment and activate it:\
"python -m venv venv"\
"source venv/bin/activate"
- After activating the virtual environment install all of the required packages mentioned in the requirements.txt:\
"pip install -r requirements.txt"
- Migrate:\
"python manage.py migrate"
- Run
"python manage.py runserver"
- Go to localhost (127.0.0.1)
