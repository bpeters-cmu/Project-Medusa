from passlib.apps import custom_app_context as pwd_context
import os
import app

class User(app.db.Model):
    __tablename__ = 'User'
    id = app.db.Column('user_id',app.db.Integer , primary_key=True)
    username = app.db.Column(app.db.String(15), unique=True , index=True)
    password = app.db.Column(app.db.String(15))
    tenancy_ocid = app.db.Column(app.db.String(128))
    user_ocid = app.db.Column(app.db.String(128))
    fingerprint = app.db.Column(app.db.String(128))
    private_key_path = app.db.Column(app.db.String(128))
    region = app.db.Column(app.db.String(50))

    def __init__(self, username, password, tenancy_ocid, user_ocid, fingerprint, private_key, region):
        self.username = username
        self.password = hash_password(password)
        self.tenancy_ocid = tenancy_ocid
        self.user_ocid = user_ocid
        self.fingerprint = fingerprint
        self.region = region

    def hash_password(self, pword):
        self.password = pwd_context.encrypt(pword)

    def verify_password(self, pword):
        return pwd_context.verify(pword, self.password)

    def insert(self):
        try:
            app.db.session.add(self)
            app.db.session.commit()
        except BaseException as e:
            print('exception occurred, rolling back app.db')
            print(str(e))
            app.db.session.rollback()


    def create_key_file(self, private_key):
        path = '/home/opc/.oci'
        filename = self.username + '.pem'

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            if os.path.join(path,filename).exists():
                return
            with open(os.path.join(path, filename), 'wb') as key_file:
                key_file.write(buff)
        except BaseException as e:
            print('Error: ' + str(e))
            return
        self.private_key_path = path + '/' + filename



#tenancy_ocid, user_ocid, fingerprint, private_key_path, region
