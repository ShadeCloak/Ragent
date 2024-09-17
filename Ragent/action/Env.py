from typing import List, Dict, Any

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
            result = method(**parameters)
        except Exception as e:
            return f"{name},错误：{str(e)}"
        return result

