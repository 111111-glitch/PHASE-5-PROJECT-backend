from models import Product, ProductOrder, ProductOrderItem, Service, ServiceOrder, ServiceOrderItem

def test_product_order_item_relationships():
    # Create sample data
    product = Product(name="Test Product", description="Test Description", price=10.0, image_url="test_image.jpg", quantity_available=5)
    product_order = ProductOrder(total_price=50.0, status="Pending")
    product_order_item = ProductOrderItem(quantity=2, product_order=product_order, product=product)

    # Test relationships
    assert product_order_item.product_order == product_order
    assert product_order_item.product == product

def test_service_order_item_relationships():
    # Create sample data
    service = Service(name="Test Service", description="Test Description", price=50.0, image_url="test_image.jpg", duration=60)
    service_order = ServiceOrder(total_price=100.0, status="Pending")
    service_order_item = ServiceOrderItem(quantity=1, service_order=service_order, service=service)

    # Test relationships
    assert service_order_item.service_order == service_order
    assert service_order_item.service == service

def run_tests():
    test_product_order_item_relationships()
    test_service_order_item_relationships()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
