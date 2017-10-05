from passlib.hash import pbkdf2_sha256 as phash
import os
from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(25), unique=True , index=True)
    password = db.Column(db.String(128))
    tenancy_ocid = db.Column(db.String(128))
    user_ocid = db.Column(db.String(128))
    fingerprint = db.Column(db.String(128))
    private_key_path = db.Column(db.String(128))
    region = db.Column(db.String(50))

    def __init__(self, username, password, tenancy_ocid, user_ocid, fingerprint, private_key, region):
        self.username = username
        self.password = self.hash_password(password)
        self.tenancy_ocid = tenancy_ocid
        self.user_ocid = user_ocid
        self.fingerprint = fingerprint
        self.region = region

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print('verifying password: ' + pword)
        print('self' + self)
        print(phash.verify(pword, self.password))
        return phash.verify(pword, self.password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()


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

    def __str__(self):
        return self.username + ' ' + self.password




#tenancy_ocid, user_ocid, fingerprint, private_key_path, region
