from uuid import uuid4

import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework.serializers import ModelSerializer

from core.apps.responses.models import Response
from core.apps.responses.paginations import ResponsePagination

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.response(type="pagination"),
]


class MockResponsSerializer(ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "content",
        ]


class TestResponseViewPagination:
    def test_paginated_correct(
        self, authenticated_client, mocker, response_factory, assert_paginated_correct
    ):
        # Arrange: mock ResponseListCreateView's get_queryset
        # Arrange: Givne there are 22 responses
        response_total_num = 22
        resposnes = response_factory.build_batch(size=response_total_num)

        (
            mocker.patch.multiple(
                "core.apps.responses.views.ResponseListCreateView",
                get_queryset=mocker.Mock(return_value=MockSet(*resposnes)),
                ordering=[],
                get_serializer_class=mocker.Mock(return_value=MockResponsSerializer),
            ),
        )

        # Arrange:
        default_page_size = ResponsePagination.page_size
        max_page_size = ResponsePagination.max_page_size
        query_param = ResponsePagination.page_size_query_param

        scenarios = [
            ("", default_page_size),
            (12, 12),
            (21, max_page_size),
        ]
        for query_num, expected_num in scenarios:
            query = {query_param: query_num}
            # Act
            resp = authenticated_client.get(
                reverse("top_level_response_list_create", args=[uuid4()]), data=query
            )

            assert len(resp.data["results"]) == expected_num
            assert_paginated_correct(
                resp=resp,
                query_num=query_num,
                paginator=ResponsePagination,
                total_count=response_total_num,
            )
