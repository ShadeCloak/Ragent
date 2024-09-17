from Ragent.prompt.prompt import prompt_to_tool
import json

class ReAct:
    def __init__(self, llm, env, protocol, max_turn = 5):
        """
        """
        self.llm = llm
        self.env = env
        self.protocol = protocol
        self.max_turn = max_turn
        self.state = []

    def add_to_state(self, role, content):
        """
        """
        self.state.append({"role": role, "content": content})

    def run(self, inputs = None):
        """
        """
        self.add_to_state(role = "user", content = f"{inputs},{prompt_to_tool}")

        for turn in range(self.max_turn):
            print(f"正在进行第 {turn + 1} 轮对话...")  # 打印当前轮次

            filename = f"{turn}_state.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=4)
            print(f"当前轮次的状态已保存到 {filename}")

            llm_response = self.llm.generate(self.state)
            #print(f"llm_response:{llm_response}")
            response = llm_response['choices'][0]['message']['content']
            self.add_to_state(role = "assistant", content = response)
            
            #print(f"response:{response}")
            message, action = self.protocol.parse(response)
            #print(f"message:{message}")
           # print(f"action:{action}")
            if action is None:
                return message

            try:
                env_response = self.env(action['name'], action['parameters'])
            except Exception as e:
                env_response = f"Error during environment interaction: {str(e)}"
            
            #print(f"Environment: {env_response}")
            with open("env_response.json", "w", encoding="utf-8") as f:
                json.dump(env_response, f, ensure_ascii=False, indent=4)

            def convert_to_paragraph(data):
                paragraph = []
                for key, value in data.items():
                    snippet = value.get("snippet", "")
                    if snippet:
                        paragraph.append(snippet)
                return " ".join(paragraph)

            # 使用该函数
            paragraph = convert_to_paragraph(env_response)
            self.add_to_state(role = 'user', content=paragraph)

            

        return "Not finished"