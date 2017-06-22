#!flask/bin/python

from app import app
print('******************* %s ******************' % app)
app.run(debug=True)
