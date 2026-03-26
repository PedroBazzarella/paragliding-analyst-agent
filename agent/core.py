from agent.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.runnables import Runnable
from langgraph.checkpoint.memory import InMemorySaver

from tools.get_weather import get_weather
from tools.get_wind_conditions import get_wind_conditions
from tools.get_paragliding_conditions import get_paragliding_conditions

llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=OLLAMA_MODEL,
    temperature=0.2
)

tools = [
    get_weather,
    get_wind_conditions,
    get_paragliding_conditions,
]

checkpointer = InMemorySaver()

system_prompt = "You are a funny paragliding assistant."

agent: Runnable = create_agent(
    model = llm,
    tools = tools,
    system_prompt = system_prompt,
    checkpointer = checkpointer,
)

def build_agent(checkpointer: InMemorySaver) -> Runnable:
    return create_agent(
        model=llm,
        tools=tools,
        system_prompt = system_prompt,
        checkpointer = checkpointer,
    )

def chat_llm():
    while True:
        prompt = input("User: ")

        if(prompt.lower() == "exit"):
            break

        print("AI: [Thinking...]")

        for chunk in agent.stream(
            {'messages': [{'role': 'user', 'content': prompt}]},
            {"configurable": {"thread_id": "1"}},
        ):
            if 'model' in chunk:
                message = chunk['model']['messages'][0]
                
                if message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"[Tool Call] {tool_call['name']} → args: {tool_call['args']}")
                else:
                    print(f"[Result]\n{message.content}")

            elif 'tools' in chunk:
                tool_msg = chunk['tools']['messages'][0]
                print(f"[Tool Result] {tool_msg.name}: {tool_msg.content}")