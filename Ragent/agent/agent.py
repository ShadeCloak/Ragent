from Ragent.prompt.prompt import prompt_to_tool_instructions
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
        actions_info = self.env.get_actions_info()
        print(f"actions_info:{actions_info}")
        self.add_to_state(
            role = "user", 
            content = f"问题如下：{inputs}可以使用的工具描述如下：{actions_info}工具使用示例如下：{prompt_to_tool_instructions}"
        )

        for turn in range(self.max_turn):
            print(f"正在进行第 {turn + 1} 轮对话...")

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

            used_tool_info = self.env.get_tool_description(action['name'])


            try:
                env_response = self.env(action['name'], action['parameters'])
            except Exception as e:
                env_response = f"Error during environment interaction: {str(e)}"
            
            #print(f"Environment: {env_response}")
            with open("env_response.json", "w", encoding="utf-8") as f:
                json.dump(env_response, f, ensure_ascii=False, indent=4)

            self.add_to_state(role = 'user', content=f"在上一轮工具选择调用的工具及其工具描述如下：{used_tool_info}.调用之后，得到如下结果：{env_response}")

            

        return "Not finished"