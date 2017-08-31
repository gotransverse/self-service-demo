from app import db

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    accountID = db.Column(db.String(8), index=True)
    apiKey = db.Column(db.String(64))
    useEnv = db.Column(db.String(16))

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __init__(self, username, password, email, accountID, apiKey, useEnv):
        """"""
        self.username = username
        self.password = password
        self.email = email
        self.accountID = accountID
        self.apiKey = apiKey
        self.useEnv = useEnv

class Server(db.Model):

    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True)
    prodURL = db.Column(db.String(32), index=True)
    envName = db.Column(db.String(16), index=True, unique=True)
    accountID = db.Column(db.String(8), index=True)
    apiKey = db.Column(db.String(64))

    def __init__(self, prodURL, envName, accountID, apiKey):
        """"""
        self.prodURL = prodURL
        self.envName = envName
        self.accountID = accountID
        self.apiKey = apiKey
