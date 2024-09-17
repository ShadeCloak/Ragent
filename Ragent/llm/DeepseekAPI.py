import requests
import json

class DeepseekAPI_ori:
    def __init__(self, api_url, api_token, model_name):
        """
        """
        self.api_url = api_url
        self.api_token = api_token
        self.model_name = model_name
    
    def chat(self, input):
        """
        """

        url = "https://api.deepseek.com/chat/completions"

        payload = json.dumps({
            "messages": [
                {
                "content": "You are a helpful assistant",
                "role": "system"
                },
                {
                "content": "Hi",
                "role": "user"
                }
            ],
            "model": "deepseek-chat",
            "frequency_penalty": 0,
            "max_tokens": 2048,
            "presence_penalty": 0,
            "response_format": {
                "type": "text"
            },
            "stop": None,
            "stream": False,
            "stream_options": None,
            "temperature": 1,
            "top_p": 1,
            "tools": None,
            "tool_choice": "none",
            "logprobs": False,
            "top_logprobs": None
        })
        
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer <TOKEN>'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

# Ragnt/llm/DeepseekAPI.py
import requests

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
        #print("456")
        #print(f"response:{response}")
        result = response.json()
        #print("789")
        return result


