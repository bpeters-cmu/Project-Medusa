from passlib.hash import pbkdf2_sha256 as phash
from app import db
from Crypto.Cipher import AES
import os
import json
import base64

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
        self.private_key_path = self.create_key_file(private_key)

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print('verifying password: ' + pword)
        print(phash.verify(pword, self.password))
        return phash.verify(pword, self.password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False


    def create_key_file(self, private_key):
        path = '/home/opc/.oci'
        filename = self.username + '.pem'

        if not os.path.exists(path):
            os.makedirs(path)

        try:
            if os.path.exists(path+filename):
                return
            with open(os.path.join(path, filename), 'w') as key_file:
                key_file.write(private_key)
        except BaseException as e:
            print('Error: ' + str(e))
            return
        return path + '/' + filename

    def __str__(self):
        return self.username + ' ' + self.password

    def create_client(self, client_username, client_password, hostname):
        client = ClientUser(client_username, client_password, hostname, self.id)
        client.insert()


class ClientUser(db.Model):
    __tablename__ = 'ClientUser'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(25), unique=True , index=True)
    password = db.Column(db.String(128))
    hostname = db.Column(db.String(25))
    conn_type = db.Column(db.String(3))
    admin_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)

    def __init__(self, username, password, hostname, admin_id):
        self.username = username
        self.password = self.hash_password(password)
        self.hostname = hostname
        self.admin_id = admin_id

    def hash_password(self, pword):
        hashed = phash.hash(pword)
        print(str(hashed))
        return hashed

    def verify_password(self, pword):
        print('verifying password: ' + pword)
        print(phash.verify(pword, self.password))
        return phash.verify(pword, self.password)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except BaseException as e:
            print('exception occurred, rolling back db')
            print(str(e))
            db.session.rollback()
            return False

    def get_token(self):
        json_data = {}
        json_data['connection']['type'] = self.conn_type
        json_data['connection']['settings']['hostname'] = self.hostname
        json_data['connection']['settings']['username'] = self.username
        json_data['connection']['settings']['password'] = self.password
        token = json.dumps(json_data).encode('utf-8')

        return base64.urlsafe_b64encode(token)





#tenancy_ocid, user_ocid, fingerprint, private_key_path, region
