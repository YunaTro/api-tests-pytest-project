from api.base_api_client import BaseApiClient

class ObjectsApiClient(BaseApiClient):
    def get_object(self, object_id):
        return self.request("GET", f"/objects/{object_id}")

    def create_object(self, payload):
        return self.request("POST", f"/objects", json=payload)

    def update_object(self, object_id, payload):
        return self.request("PATCH", f"/objects/{object_id}", json=payload)

    def delete_object(self, object_id):
        return self.request("DELETE", f"/objects/{object_id}")
