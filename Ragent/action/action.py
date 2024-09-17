import requests
from Ragent.action.base_action import tool_api  # 假设这个装饰器在该路径下
import json

class Env:
    def __init__(self, tools):
        """
        """
        self.tools = {
            tool.name : tool for tool in tools
        }

    def get_actions_info(self):
        """
        """
        actions_info = []
        for tool_name, tool in self.tools.items():
            actions_info.append({
                'name' : tool_name,
                'description' : tool.__doc__
            })
        return actions_info

    def __call__(self, name, parameters):
        """
        """
        if '.' in name:
            action_name, method_name = name.split('.')
        else:
            action_name = name
            method_name = 'run'

        action = self.tools.get(action_name)
        if not action:
            return f"Action {action_name}不存在"

        method = getattr(action, method_name, None)
        if not method :
            return f"Action {action_name}没有方法{method_name}"

        try:
            #print("666")
            #print(parameters)
            #print(method)
            result = method(**parameters)
            #print("777")
        except Exception as e:
            return f"{name},错误：{str(e)}"
        return result

class WebSearch:
    def __init__(self, api_url = '', api_key = ''):
        """
        """
        self.name = 'Websearch'
        self.api_url = api_url = 'https://google.serper.dev/search'
        self.api_key = api_key = 'fd613dd0673ca3a2ebacf1ee9f04b1caf1810305'
        self.search_results = {}

    @tool_api
    def search(self, query):
        """
        """
        #print(f"query:{query}")
        payload = json.dumps({
            "q": query,
            "hl": "zh"
        })
        params = {
            'q': query,
            'count': 1,
            "hl": "zh"
        }
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        """
        response = requests.get(
            self.api_url, headers = headers, params = params
        )
        """
        response = requests.request("POST", self.api_url, headers=headers, data=payload)
        #print(f"response:{response}")
        response.raise_for_status()
        
        print(f"Response Status Code: {response.status_code}")

        data = response.json()
        #print(f"data:{data}")
        with open("google.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        organic_results = data.get('organic', [])

        self.search_results = {
            i: {
                'url': item.get('link', ''),      
                'title': item.get('title', ''),   
                'snippet': item.get('snippet', '')
            } for i, item in enumerate(organic_results)
        }

        return self.search_results

    @tool_api
    def select(self, select_ids):
        """
        """
        selectde_results = {}
        for idx in select_ids:
            selectde_results[idx] = self.search_results[idx]
        return selectde_results

