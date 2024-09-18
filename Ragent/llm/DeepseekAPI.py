import requests
import json


class DeepseekAPI:
    def __init__(self, api_url, api_token, model_name):
        """
        
        """
        self.api_token = api_token
        self.api_url = api_url
        self.model_name = model_name

    def generate(self, input_text):
        """
        """
        payload = json.dumps({
            "messages" : input_text,
            "model" : self.model_name
        })
        #print("123")
        headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'Authorization' : f'Bearer {self.api_token}',
        }
        response = requests.post(self.api_url, headers = headers, data = payload)
        #print(f"response:{response}")
        result = response.json()
        return result


