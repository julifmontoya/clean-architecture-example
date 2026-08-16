# modules/catalog/application/use_cases/create_category.py
from modules.catalog.models import Category


class CreateCategory:
    def execute(self, title: str) -> Category:
        category = Category(title=title)
        category.save()
        return category