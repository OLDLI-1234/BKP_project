from db import db
class Hourse_info(db.Model):
    __tablename__='hourse_info'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(255),nullable=False)
    cover=db.Column(db.String(2555),nullable=False)
    city=db.Column(db.String(255),nullable=False)
    region=db.Column(db.String(255),nullable=False)
    address=db.Column(db.String(2555),nullable=False)
    rooms_desc=db.Column(db.String(255),nullable=False)
    area_range=db.Column(db.String(255),nullable=False)
    all_ready=db.Column(db.String(255),nullable=False)
    price=db.Column(db.String(255),nullable=False)
    hourseDecoration=db.Column(db.String(255),nullable=False)
    company=db.Column(db.String(255),nullable=False)
    hourseType=db.Column(db.String(255),nullable=False)
    on_time=db.Column(db.String(255),nullable=False)
    open_date=db.Column(db.String(255),nullable=False)
    tags=db.Column(db.String(255),nullable=False)
    totalPrice_range=db.Column(db.String(255),nullable=False)
    sale_status=db.Column(db.String(255),nullable=False)
    detail_url=db.Column(db.String(2555),nullable=False)
