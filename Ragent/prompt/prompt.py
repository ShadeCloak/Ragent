
prompt_to_tool_instructions = """
{used_tool_info}
在需要调用工具时，使用特定格式来标记工具调用:

要求：
- 如果需要调用工具，请用以下格式标记工具调用：
  <|FunctionCallBegin|>
  {{
    "name": "工具名",
    "parameters": {{
      "query": "问题描述"
    }}
  }}
  <|FunctionCallEnd|>

示例 1：
  <|FunctionCallBegin|>
  {{
    "name": "Websearch.search",
    "parameters": {{
      "query": "the most beautiful city"
    }}
  }}
  <|FunctionCallEnd|>

示例 2：
  <|FunctionCallBegin|>
  {{
    "name": "Websearch.select",
    "parameters": {{
      "select_ids": [1, 3]
    }}
  }}
  <|FunctionCallEnd|>

请注意：确保回答中包含清晰的标记，并且在需要时准确地指定工具和参数。一定记住每次只能选择一个工具调用。
"""
