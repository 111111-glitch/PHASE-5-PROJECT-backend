from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OrderItem(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # serialize_rules = ('-order.order_items', '-product.orders',)

    def __repr__(self):
        return f'<OrderItem {self.id}>'
    


class ServiceOrderItem(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)

    def __repr__(self):
        return f'<ServiceOrderItem {self.id}>'

