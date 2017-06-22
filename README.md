# weather_forecasts
An experiment in Python. Add zip codes to a database and retrieve weather forecasts for them.


Initial Setup
---

```
git clone https://github.com/clarkdowner/weather_forecasts.git
cd weather_forecasts
python -m venv flask
flask/Scripts/pip install -r requirements.txt
flask/Scripts/python ./db_create.py
```


Usage
---

1. Run Python interpreter:
```
flask/Scripts/python
```

2. Add zip to database:
```
>>> from app import db, models
>>> l = models.Location(zip='94107', name='San Francisco')
>>> db.session.add(l)
>>> db.session.commit()
```

3. Start Flask server on port 5000:
```
flask/Scripts/python run.py
```

4. Profit
