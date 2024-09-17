import json

class BaseProtocol:
    def __init__(self, special_tokens=dict(action_start_token='', action_end_token='')):
        # 初始化时传入的特殊 token 字典
        self.special_tokens = special_tokens

    def parse(self, text):
        """
        Parses the LLM response to extract plain text and action call if any.
        :param text: The response from the LLM.
        :return: A tuple of the parsed text and an action dictionary (or None if no action).
        """
        # 检查是否包含 action_start_token
        if self.special_tokens['action_start_token'] in text:
            # 拆分出普通文本和 action 部分
            text, action_str = text.split(self.special_tokens['action_start_token'])
            action_str = action_str.split(self.special_tokens['action_end_token'])[0]

            try:
                # 尝试将 action_str 解析为 JSON 格式的 action
                action = json.loads(action_str)
            except json.JSONDecodeError:
                # 如果 action_str 以 ``` 开头，则为代码执行任务
                if action_str.startswith('```'):
                    action = dict(
                        name='PythonInterpreter',
                        parameters=dict(code=action_str.strip('```'))  # 提取代码内容
                    )
                else:
                    action = None
        else:
            action = None

        # 返回普通文本和 action
        return text.strip(), action


class deepseekProtocol(BaseProtocol):
    def __init__(self, special_tokens=dict(action_start_token='<|FunctionCallBegin|>', action_end_token='<|FunctionCallEnd|>')):
        super().__init__(special_tokens)

    def create_prompt(self, query, task_type=None):
        """
        Create a formatted prompt for the LLM based on the user query and optional task type.
        :param query: The user input query.
        :param task_type: Optional task type, e.g., 'search', 'execute code'.
        :return: The formatted prompt for the LLM.
        """
        return f"User asks: {query}\nIf you don't know the answer, please use a search tool to find the relevant data. Provide a detailed comparison."
