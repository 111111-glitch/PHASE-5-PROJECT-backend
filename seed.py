from app import db, app
from models import Product,Service,Admin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def seed_data():
    with app.app_context():

        print('Deleting existing products...')
        Product.query.delete()
        Service.query.delete()
        Admin.query.delete()


        print('Creating products...')

        seller_id = 1  # Set the seller_id to 1 for all products

        phone1 = Product(name='iPhone 14 Prp', price=999, description='Apple iPhone 14 Pro, 128GB, Purple', image_url='https://i.pinimg.com/564x/46/4a/3c/464a3c2e8af440f769de8456976ffbc7.jpg', quantity_available=100, seller_id=seller_id)
        phone2 = Product(name='Samsung Galaxy S20', price=799, description='Samsung Galaxy S20, 128GB, Cosmic Gray', image_url='https://i.pinimg.com/564x/e8/b2/7d/e8b27df6b3f8f76c569c1715297672d2.jpg', quantity_available=80, seller_id=seller_id)
        phone3 = Product(name='Google Pixel 5', price=699, description='Google Pixel 7a, 128GB, Just Black', image_url='https://i.pinimg.com/564x/df/c7/24/dfc72427002660c11845df1c3e6cf43b.jpg', quantity_available=120, seller_id=seller_id)
        phone4 = Product(name='OnePlus 9 Pro', price=899, description='OnePlus 9 Pro, 256GB, Morning Mist', image_url='https://i.pinimg.com/564x/a2/c9/61/a2c9612d875b39b0d899598b67dc415d.jpg', quantity_available=90, seller_id=seller_id)

        laptop1 = Service(name='MacBook Pro', price=1799, description='Apple MacBook Pro, 13-inch, M1 chip, 256GB SSD', image_url='https://i.pinimg.com/736x/69/d5/44/69d544b42b46e696650e07ddef8bd28e.jpg', duration=110, seller_id=seller_id)
        laptop2 = Service(name='Dell XPS 15', price=1499, description='Dell XPS 15 9500, Intel Core i7, 16GB RAM, 512GB SSD', image_url='https://i.pinimg.com/564x/e7/f8/01/e7f801cef4b945026ee53d3d8ebc3906.jpg', duration=95, seller_id=seller_id)
        laptop3 = Service(name='HP Spectre x360', price=1299, description='HP Spectre x360, 13.3-inch 4K OLED, Intel Core i7, 512GB SSD', image_url='https://i.pinimg.com/564x/1a/c6/81/1ac681ab418ea8dfd00e37c3b2580fe1.jpg', duration=125, seller_id=seller_id)
        laptop4 = Service(name='Lenovo ThinkPad X1 Carbon', price=1399, description='Lenovo ThinkPad X1 Carbon Gen 9, Intel Core i5, 256GB SSD', image_url='https://i.pinimg.com/564x/d7/10/f1/d710f17efbfcaa72651a2c6930c5e0ad.jpg', duration=105, seller_id=seller_id)


        admin1 = Admin(username='MacBook Pro', email="jondoe@gmail.com", password=bcrypt.generate_password_hash('Applecider'), role='admin')
        admin2 = Admin(username='Mac Bouy', email="markdoe@gmail.com", password=bcrypt.generate_password_hash('Applecider'), role='admin')

        
        admins = [admin1, admin2]
        products = [phone1, phone2, phone3, phone4]
        services = [laptop1, laptop2, laptop3, laptop4]

        # Combine all the objects into a single iterable
        objects_to_add = admins + products + services

        # Add all objects to the session
        db.session.add_all(objects_to_add)

        # Commit the changes
        db.session.commit()


        print('Successfully created products')

if __name__ == '__main__':
    seed_data()
