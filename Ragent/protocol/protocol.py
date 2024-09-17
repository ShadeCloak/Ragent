import json

class BaseProtocol:
    def __init__(self, special_tokens = dict(action_start_token = '', action_end_token = '')):
        """
        """
        self.special_tokens = special_tokens

    def parse(self, text):
        """
        """
        start_token = self.special_tokens['action_start_token']
        end_token = self.special_tokens['action_end_token']

        if start_token in text and end_token in text:
            # 提取 action_str 的部分
            try:
                parts = text.split(start_token, 1)
                action_str = parts[1].split(end_token, 1)[0].strip()
                #print("666")
                #print(action_str)

                # 处理 action_str
                if isinstance(action_str, str):
                    action = json.loads(action_str)
                    #print("666",action)
                else:
                    action = None
            except (IndexError, json.JSONDecodeError) as e:
                action = None
        else:
            action = None
        
        # 提取剩余的 text 部分
        text = text.split(start_token, 1)[0].strip()
        return text, action



class deepseekProtocol(BaseProtocol):
    def __init__(self, special_tokens = dict(action_start_token = '<|FunctionCallBegin|>', action_end_token = '<|FunctionCallEnd|>')):
        super().__init__(special_tokens)

    def create_prompt(self, query, task_type = None):
        if task_type:
            return f"User asks: {query}\nTask type: {task_type}\nIf you don't know the answer, please use a search tool to find the relevant data. Provide a detailed comparison."
        else:
            return f"User asks: {query}\nIf you don't know the answer, please use a search tool to find the relevant data. Provide a detailed comparison."

