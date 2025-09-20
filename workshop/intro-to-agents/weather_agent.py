import asyncio
from weather_tools import tools
from dapr_agents import Agent, HFHubChatClient
from dotenv import load_dotenv
from dapr_agents.memory import ConversationDaprStateMemory


load_dotenv()

llm = HFHubChatClient(model="HuggingFaceTB/SmolLM3-3B")

AIAgent = Agent(
    name="Stevie",
    role="Weather Assistant",
    goal="Assist Humans with weather related tasks.",
    instructions=[
        "Always answer the user's main weather question directly and clearly.",
        "If you perform any additional actions, summarize those actions and their results.",
        "At the end, provide a concise summary that combines the weather information for all requested locations and any other actions you performed.",
    ],
    llm=llm,
    tools=tools,
    memory=ConversationDaprStateMemory(store_name="historystore", session_id="some-id")
)

async def main():
    await AIAgent.run("What is the weather in Amsterdam and Madrid?")
    
    print("Chat history after first interaction:")
    print(AIAgent.chat_history)

    # # Second interaction (agent will remember the first one)
    # await AIAgent.run("How about in Seattle?")

    # # View updated history
    # print("Chat history after second interaction:")
    # print(AIAgent.chat_history)

    # # Reset memory
    # AIAgent.reset_memory()
    # print("Chat history after reset:")
    # print(AIAgent.chat_history)  # Should be empty now


if __name__ == "__main__":
    asyncio.run(main())