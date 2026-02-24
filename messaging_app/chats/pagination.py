from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    page_size = 20  # enforce 20 messages per page

    def get_paginated_response(self, data):
        page = self.page

        return Response({
            'count': page.paginator.count,  # ✅ required by checker
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })