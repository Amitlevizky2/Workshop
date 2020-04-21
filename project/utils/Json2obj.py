import json
import jsonpickle

from project.domain_layer.stores_managment.Product import Product


def product_to_json(p: Product) -> json:
    return jsonpickle.encode(p)


def json_to_product(json_product: Product) -> Product:
    return jsonpickle.decode(json_product)
