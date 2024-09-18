import requests
from Ragent.action.base_action import tool_api
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
            for method_name in dir(tool):
                method = getattr(tool, method_name)
                if method_name.startswith('_') or not callable(method):
                    continue
                full_name = f"{tool_name}.{method_name}"
                actions_info.append({
                    'name': full_name,
                    'description': method.__doc__
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
            #print(parameters)
            #print(method)
            result = method(**parameters)
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
        执行网络搜索请求，使用给定的查询关键字发送 POST 请求到 API，并返回搜索结果。
        
        参数:
        - query (str): 要进行搜索的查询关键字或问题。
        
        返回:
        - search_results (dict): 搜索结果的字典形式，包含链接、标题和摘要信息。
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
        从搜索结果中选择指定的结果条目。
        
        参数:
        - select_ids (list): 包含要选择的结果的索引列表。
        
        返回:
        - selectde_results (dict): 按选择的索引返回的搜索结果字典。
        """
        selectde_results = {}
        for idx in select_ids:
            result = self.search_results.get(idx)
            if not result:
                continue
            url = result['url']
            title = result['title']
            try:
                response = requests.get(url)
                response.raise_for_status()

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text() for p in paragraphs if p.get_text()])

                selectde_results[idx] = {
                    'url': url,
                    'title': title,
                    'content': content[:1000]
                }
            except Exception as e:
                selectde_results[idx] = {
                    'url': url,
                    'title': title,
                    'error': f"Failed to fetch content: {str(e)}"
                }

        with open("select.json", "w", encoding="utf-8") as f:
            json.dump(selectde_results, f, ensure_ascii=False, indent=4)

        return selectde_results

