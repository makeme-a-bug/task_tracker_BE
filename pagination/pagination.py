from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


#issue: shows all pages when page_size is set to 0
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'




#pagination function for custom action in viewsets
def response_with_paginator(viewset, queryset):
    page = viewset.paginate_queryset(queryset)
    if page is not None:
        serializer = viewset.get_serializer(page, many=True)
        return viewset.get_paginated_response(serializer.data)

    return Response(viewset.get_serializer(queryset, many=True).data)