class Product:
    def __init__(self, id, name, price, brand, description, category, attributes, filename, s3_url=None):
        self.id = id
        self.name = name
        self.price = price
        self.brand = brand
        self.description = description
        self.category = category
        self.attributes = attributes
        self.filename = filename
        self.s3_url = s3_url

