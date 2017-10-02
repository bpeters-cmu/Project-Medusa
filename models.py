from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column(db.String(15), unique=True , index=True)
    password = db.Column(db.String(15))
    tenancy_ocid = db.Column(db.String(128))
    user_ocid = db.Column(db.String(128))
    fingerprint = db.Column(db.String(128))
    private_key_path = db.Column(db.String(128))
    region = db.Column(db.String(50))



#tenancy_ocid, user_ocid, fingerprint, private_key_path, region
