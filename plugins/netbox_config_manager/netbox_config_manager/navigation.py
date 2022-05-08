from . import simple_models

menu_items = [
]

for m in simple_models.MODEL_REGISTRY:
    menu_items.append(m.generate_navigation())
