import pytest
import os
from wiremock.constants import Config
from wiremock.server.server import WireMockServer
from wiremock.client import (
    Mapping,
    MappingRequest,
    MappingResponse,
    HttpMethods,
    Mappings,
)


WIREMOCK_URL = "http://localhost:8000"


def get_products():
    return [
        {"name": "Mock Product A", "price": 10.99, "category": "Books"},
        {"name": "Mock Product B", "price": 5.99, "category": "Movies"},
        {"name": "Mock Product C", "price": 7.99, "category": "Electronics"},
        {"name": "Mock Product D", "price": 12.99, "category": "Books"},
        {"name": "Mock Product E", "price": 8.99, "category": "Movies"},
        {"name": "Mock Product F", "price": 15.99, "category": "Electronics"},
    ]


def get_mappings() -> list[Mapping]:
    return [
        Mapping(
            priority=100,
            request=MappingRequest(method=HttpMethods.GET, url="/hello"),
            response=MappingResponse(status=200, body="hello"),
            persistent=False,
        ),
        Mapping(
            priority=100,
            request=MappingRequest(method=HttpMethods.GET, url="/products"),
            response=MappingResponse(status=200, json_body=get_products()),
            persistent=False,
        ),
        Mapping(
            priority=100,
            request=MappingRequest(
                method=HttpMethods.GET,
                url=r"/products?category=Books",
                query_parameters={"category": {"equalTo": "Books"}},
            ),
            response=MappingResponse(
                status=200,
                json_body=list(
                    filter(lambda p: p["category"] == "Books", get_products())
                ),
            ),
            persistent=False,
        ),
    ]


@pytest.fixture
def wm_url():
    yield WIREMOCK_URL


@pytest.fixture
def wm_java():
    with WireMockServer() as _wm:
        Config.base_url = f"{WIREMOCK_URL}/__admin"
        os.environ["PRODUCTS_SERVICE_HOST"] = f"{WIREMOCK_URL}"
        [Mappings.create_mapping(mapping=mapping) for mapping in get_mappings()]

        yield _wm

        Mappings.delete_all_mappings()
