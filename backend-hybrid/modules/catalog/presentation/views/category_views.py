from rest_framework.response import Response
from rest_framework.views import APIView

from modules.catalog.application.use_cases.create_category import CreateCategory
from modules.catalog.application.use_cases.list_categories import ListCategories
from modules.catalog.presentation.serializers.category_serializer import CategorySerializer


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = ListCategories().execute()
        return Response(CategorySerializer(categories, many=True).data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CreateCategory().execute(serializer.validated_data["title"])

        return Response(CategorySerializer(category).data, status=201)