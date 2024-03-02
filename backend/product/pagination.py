from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20  # Set numbers of items per page
    page_query_param = 'p'  # Set page query param name
