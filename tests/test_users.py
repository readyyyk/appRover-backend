from pytest import mark
from randomuser import RandomUser
from fastapi import status
from httpx import AsyncClient
from .config import token_stack, id_stack, token_refresh_stack


class TestUser:
    @mark.dependency(name='test_create')
    async def test_create_user(self, random_user: RandomUser, t_client: AsyncClient):
        response = await t_client.post(
            '/users/create',
            json={
                'username': random_user.get_username(),
                'password': random_user.get_password()
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert 'user_id' in response_data and 'access_token' in response_data and 'refresh_token' in response_data
        global id_stack
        id_stack = response.json()['user_id']

    @mark.dependency(name='test_auth_user', depends=['test_create'])
    async def test_auth_user(self, random_user: RandomUser, t_client: AsyncClient):
        response = await t_client.post(
            '/auth/login',
            data={
                'username': random_user.get_username(),
                'password': random_user.get_password()
            }
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert 'access_token' in response_data and 'refresh_token' in response_data
        global token_stack
        global token_refresh_stack
        token_stack = response_data['access_token']
        token_refresh_stack = response_data['refresh_token']

    @mark.dependency(name='test_get_me', depends=['test_create', 'test_auth_user'])
    async def test_get_me(self, t_client: AsyncClient, random_user: RandomUser):
        response = await t_client.get(
            '/users/me',
            headers={
                'Authorization': f'Bearer {token_stack}'
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == random_user.get_username()

    @mark.dependency(name='test_refresh', depends=['test_get_me'])
    async def test_refresh(self, t_client: AsyncClient):
        response = await t_client.get(
            '/auth/refresh',
            headers={
                'Authorization': f'Bearer {token_refresh_stack}'
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.json()

    @mark.dependency(name='test_get_user', depends=['test_create'])
    async def test_get_user(self, t_client, random_user: RandomUser):
        response = await t_client.get(
            f'/users/{id_stack}'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['username'] == random_user.get_username()
