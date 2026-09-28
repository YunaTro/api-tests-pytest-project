from config import BASE_URL
from api.base_api_client import BaseApiClient

class ObjectsApiClient(BaseApiClient):
    def get_object(self, object_id):
        return self.request("GET", f"/objects/{object_id}")

def get_object(api_client, object_id):
    return api_client.get(
        f"{BASE_URL}/objects/{object_id}",
        timeout=(3, 15)
    )

def create_object(api_client, payload):
    return api_client.post(
        f"{BASE_URL}/objects",
        json=payload,
        timeout=(3, 15)
    )

def update_object(api_client, object_id, payload):
    return api_client.patch(
        f"{BASE_URL}/objects/{object_id}",
        json=payload,
        timeout=(3, 15)
    )


def delete_object(api_client, object_id):
    return api_client.delete(
        f"{BASE_URL}/objects/{object_id}",
        timeout=(3, 15)
    )
