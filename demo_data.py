from app import db,models

user = models.User(username='admin', password='[secure_password]', email='[your_email]', accountID='[default_account]', apiKey='XXXXXXXXXXXXXXXXX', useEnv='Env1')
db.session.add(user)

user = models.User(username='Billing User', password='[secure_password]', email='[your_email]', accountID='[default_account]', apiKey='XXXXXXXXXXXXXXXXX', useEnv='Env1')
db.session.add(user)

user = models.User(username='View User', password='[secure_password]', email='[your_email]', accountID='[default_account]', apiKey='XXXXXXXXXXXXXXXXX', useEnv='Env1')
db.session.add(user)

server = models.Server(prodURL='https://[your_server]', envName='Env1', accountID='XX', apiKey='XXXXXXXXXXXXXXXX')
db.session.add(server)

server = models.Server(prodURL='https://[your_server]', envName='Env2', accountID='XX', apiKey='XXXXXXXXXXXXXXXX')
db.session.add(server)

server = models.Server(prodURL='https://[your_server]', envName='Env3', accountID='XX', apiKey='XXXXXXXXXXXXXXXX')
db.session.add(server)

# commit the record the database
db.session.commit()

users = models.User.query.all()

for u in users:
    print(u.id,u.username)

servers = models.Server.query.all()

for s in servers:
    print(s.id,s.envName, s.prodURL)