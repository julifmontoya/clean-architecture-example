from modules.catalog.models import Category


class ListCategories:
    def execute(self) -> list[Category]:
        return list(Category.objects.all())
