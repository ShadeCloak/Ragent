from Ragent.agent.agent import ReAct
from Ragent.action.action import WebSearch, Env
from Ragent.llm.DeepseekAPI import DeepseekAPI
from Ragent.protocol.protocol import deepseekProtocol

import json

model_name = 'deepseek-chat'
api_url = "https://api.deepseek.com/chat/completions"

api_token = "sk-2604f83f3b364492aa891a7f717e265c"
"""
deepseek_api = DeepseekAPI(api_url, api_token, model_name)
response = deepseek_api.generate("告诉我北京2024年9月1日的天气")

with open("example.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

"""
env = Env([WebSearch()])

llm = DeepseekAPI(
    api_url = api_url,
    api_token = api_token,
    model_name = model_name
)

protocol = deepseekProtocol()

agent = ReAct(
    llm=llm,
    env=env,
    protocol=protocol
)

response = agent.run("请上网查询阿里巴巴在 2023 年的电商业务交易额是多少？同时对比一下京东在同年的电商业务交易额？")

print(response)





