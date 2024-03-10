import pytest
from starlette import status

from models import Place
from repositories.places_repository import PlacesRepository


@pytest.mark.usefixtures("session")
class TestPlacesCreateMethod:
    """
    Тестирование метода создания любимого места.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.

        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_method_success(self, client, session, httpx_mock):
        """
        Тестирование успешного сценария.

        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :param httpx_mock: Фикстура запроса на внешние API.
        :return:
        """

        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }
        # замена настоящего ответа от API на "заглушку" для тестирования
        # настоящий запрос на API не производится
        httpx_mock.add_response(json=mock_response)

        # передаваемые данные
        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание тестового места",
        }
        # осуществление запроса
        response = await client.post(
            await self.get_endpoint(),
            json=request_body,
        )

        # проверка корректности ответа от сервера
        assert response.status_code == status.HTTP_201_CREATED

        response_json = response.json()
        assert "data" in response_json
        assert isinstance(response_json["data"]["id"], int)
        assert isinstance(response_json["data"]["created_at"], str)
        assert isinstance(response_json["data"]["updated_at"], str)
        assert response_json["data"]["latitude"] == request_body["latitude"]
        assert response_json["data"]["longitude"] == request_body["longitude"]
        assert response_json["data"]["description"] == request_body["description"]
        assert response_json["data"]["country"] == mock_response["countryCode"]
        assert response_json["data"]["city"] == mock_response["city"]
        assert response_json["data"]["locality"] == mock_response["locality"]

        # проверка существования записи в базе данных
        created_data = await PlacesRepository(session).find_all_by(
            latitude=request_body["latitude"],
            longitude=request_body["longitude"],
            description=request_body["description"],
            limit=100,
        )
        assert len(created_data) == 1
        assert isinstance(created_data[0], Place)
        assert created_data[0].latitude == request_body["latitude"]
        assert created_data[0].longitude == request_body["longitude"]
        assert created_data[0].description == request_body["description"]
        assert created_data[0].country == mock_response["countryCode"]
        assert created_data[0].city == mock_response["city"]
        assert created_data[0].locality == mock_response["locality"]


@pytest.mark.usefixtures("session")
class TestPlacesGetMethod:
    """
    Тестирование метода получения любимых мест.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.
        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_method_list(self, client, session):
        """
        Тестирование успешного сценария.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """

        # передаваемые данные
        request_body = {"latitude": 0, "longitude": 0, "description": "string"}
        await PlacesRepository(session).create_model(request_body)
        response = await client.get(await self.get_endpoint())

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "total" in response_json
        assert isinstance(response_json["total"], int)
        assert response_json["total"] == 2

        assert "page" in response_json
        assert isinstance(response_json["page"], int)
        assert response_json["page"] == 1

        assert "size" in response_json
        assert isinstance(response_json["size"], int)
        assert response_json["size"] == 50

        assert "items" in response_json
        item = response_json["items"][0]
        assert isinstance(item["id"], int)
        assert isinstance(item["created_at"], str)
        assert isinstance(item["updated_at"], str)
        assert item["latitude"] == request_body["latitude"]
        assert item["longitude"] == request_body["longitude"]
        assert item["description"] == request_body["description"]
        assert item["country"] is None
        assert item["city"] is None
        assert item["locality"] == "Etc/GMT"


@pytest.mark.usefixtures("session")
class TestPlacesUpdateMethod:
    """
    Тестирование метода изменения любимых мест.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.
        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_method_patch(self, client, session, httpx_mock):
        """
        Тестирование успешного сценария.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :param httpx_mock: Фикстура запроса на внешние API.
        :return:
        """

        mock_response = {
            "city": "City",
            "countryCode": "AA",
            "locality": "Location",
        }
        # замена настоящего ответа от API на "заглушку" для тестирования
        # настоящий запрос на API не производится

        httpx_mock.add_response(json=mock_response)
        request_body = {
            "latitude": 15.3433,
            "longitude": 15.3433,
            "description": "Описание тестового места",
            "city": "City",
            "country": "BB",
            "locality": "Location",
        }

        model = await PlacesRepository(session).create_model(request_body)

        patch_request_body = {
            "latitude": 15.3433,
            "longitude": 15.3433,
            "description": "Описание тестового места",
        }

        response = await client.patch(
            await self.get_endpoint() + f"/{model}", json=patch_request_body
        )

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()

        assert "data" in response_json
        assert isinstance(response_json["data"], dict)
        item = response_json["data"]
        assert isinstance(item["id"], int)
        assert isinstance(item["created_at"], str)
        assert isinstance(item["updated_at"], str)
        assert item["latitude"] == patch_request_body["latitude"]
        assert item["longitude"] == patch_request_body["longitude"]
        assert item["description"] == patch_request_body["description"]
        assert item["country"] == mock_response["countryCode"]
        assert item["city"] == mock_response["city"]
        assert item["locality"] == mock_response["locality"]


@pytest.mark.usefixtures("session")
class TestPlacesDeleteMethod:
    """
    Тестирование метода изменения любимых мест.
    """

    @staticmethod
    async def get_endpoint() -> str:
        """
        Получение адреса метода API.
        :return:
        """

        return "/api/v1/places"

    @pytest.mark.asyncio
    @pytest.mark.usefixtures("event_producer_publish")
    async def test_method_delete(self, client, session):
        """
        Тестирование успешного сценария.
        :param client: Фикстура клиента для запросов.
        :param session: Фикстура сессии для работы с БД.
        :return:
        """

        # создание объекта
        request_body = {
            "latitude": 12.3456,
            "longitude": 23.4567,
            "description": "Описание тестового места",
            "city": "City",
            "country": "AA",
            "locality": "Location",
        }
        place_id = await PlacesRepository(session).create_model(request_body)

        response = await client.delete(await self.get_endpoint() + f"/{place_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await client.get((await self.get_endpoint()) + f"/{place_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
