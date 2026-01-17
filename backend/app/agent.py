from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from .tools import calculator, get_stock_price
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SYSTEM_PROMPT = """You are a helpful AI assistant.

STRICT RULES:
- You can ONLY use the tools explicitly provided to you.
- Available tools are: calculator, get_stock_price.
- NEVER call any other tool.
- NEVER attempt web search or browsing.
- If a question does not require tools, answer directly from your knowledge.

Tool usage rules:
- Use tools ONLY when required.
- Tools return raw data (numbers or JSON).
- ALWAYS convert tool results into clear, natural language sentences.
- After producing a valid final answer, STOP.
"""


tools = [calculator, get_stock_price]

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    model_kwargs={
        "tool_choice": "auto"  
    }
)

agent = create_agent(
    model=llm,
    tools=tools
)


def run_agent(messages):
    lc_messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in messages:
        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))

    response = agent.invoke(
        {"messages": lc_messages},
        config={"recursion_limit": 4}
    )

    return response["messages"][-1].content