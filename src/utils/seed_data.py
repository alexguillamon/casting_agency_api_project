from utils.gender import Gender
from datetime import date

the_date = date.today()

actors_data = [
    {
        "name": "jake",
        "DOB": the_date,
        "gender": Gender.male
    }, {
        "name": "vic",
        "DOB": the_date,
        "gender": Gender.female
    },
    {
        "name": "ella",
        "DOB": the_date,
        "gender": Gender.other
    },
    {
        "name": "pedro",
        "DOB": the_date,
        "gender": Gender.male
    },
]
movies_data = [
    {
        "title": "The Movie",
        "release_date": the_date
    }, {
        "title": "The Not Movie",
        "release_date": the_date
    }, {
        "title": "The Third Movie",
        "release_date": the_date
    },
]
