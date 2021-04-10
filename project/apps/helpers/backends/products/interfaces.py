from dataclasses import dataclass


@dataclass
class Product:
    id: str
    price: float
    image: str
    brand: str
    title: str

    def as_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'image': self.image,
            'brand': self.brand,
            'title': self.title,
        }

    @classmethod
    def from_dict(cls, data):
        return Product(
            id=data.get('id', None),
            price=float(data.get('price', 0)),
            image=data.get('image', None),
            brand=data.get('brand', None),
            title=data.get('title', None),
        )
