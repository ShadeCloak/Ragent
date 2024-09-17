prompt_to_tool = """
请根据以下要求回答问题，并在需要调用工具时，使用特定格式来标记工具调用。

要求：
- 如果需要调用工具，请用以下格式标记工具调用：
  <|FunctionCallBegin|>
  {
    "name": "工具名",
    "parameters": {
      "query": "问题描述"
    }
  }
  <|FunctionCallEnd|>


示例 1：
- 问题: “亚马逊在2023年的全球销售额是多少？”
- 回答: “亚马逊的全球销售额信息通常在其年度财报中公布。如果您需要具体的数据，请调用以下工具：
  <|FunctionCallBegin|>
  {
    "name": "Websearch.search",
    "parameters": {
      "query": "2023 Amazon global sales revenue"
    }
  }
  <|FunctionCallEnd|>”

示例 2：
- 问题: “苹果公司2023年第四季度的收入是多少？”
- 回答: “苹果公司的季度收入信息通常会在其季度财报中公布。如果您想查询最新的第四季度收入，请调用以下工具：
  <|FunctionCallBegin|>
  {
    "name": "Websearch.search",
    "parameters": {
      "query": "2023 Apple Q4 revenue"
    }
  }
  <|FunctionCallEnd|>”

请注意：确保回答中包含清晰的标记，并且在需要时准确地指定工具和参数。

"""