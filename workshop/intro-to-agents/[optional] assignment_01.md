# [Optional] Introduction to AI Agents

This assignment will provide a brief introduction to agents, tools and memory state stores in Dapr.

## What are AI Agents?

AI agents are systems that understand tasks, make decisions, and take actions autonomously. They use large language models (LLMs) as their "brain" for reasoning and planning, while leveraging external tools like APIs to access real-time information and interact with the world. Their behavior is non-deterministic—they may respond differently to the same input because LLMs can generate varied outputs, and the information they retrieve through tools may change depending on when or how they access it.

### When to Use AI Agents?

* Open-ended problems: allowing the LLM to determine needed steps to complete a task because it can't always be hardcoded into a workflow.
* Multi-step processes: tasks that require a level of complexity in which the AI agent needs to use tools or information over multiple turns instead of single shot retrieval.
* Improvement over time: tasks where the agent can improve over time by receiving feedback from either its environment or users in order to provide better utility.

### Choosing between an LLMs or an API

Use an LLM when you need:

* Explanations, general knowledge, or educational content.
* Creative writing, content generation, or brainstorming.
* Conversational interactions, personal assistance, or reminders.
* NLP tasks like summarization, sentiment analysis, and translations

Use an API when you need:

* Real-time or up-to-date information (e.g., stock prices, weather).
* Structured, specific data (e.g., country statistics, flight info).
* Access to external services (e.g., payment processing, user authentication).

## Prerequisites

1. If you haven't already, navigate to the root of the directory and install the dependencies:

<!-- STEP
name: Install Python dependencies
-->

```bash
pip install -r requirements.txt
```

In addition, install Dapr CLI and Docker Desktop:

* [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
* [Docker Desktop](https://docs.docker.com/desktop/)

<!-- END_STEP -->

2. Create a `.env` file for your API keys in `workshop/intro-to-agents/`

```env
export HUGGINGFACE_API_KEY=your_api_key_here >> .env
```

Make sure Dapr is initialized on your system:

```bash
dapr init
```

## Key Concepts

## Tool Creation and Agent Execution

First, inspect the tools in `weather_tools.py`.

### Tool Definition

* The `@tool` decorator registers functions as tools with the agent
* Each tool has a docstring that helps the LLM understand its purpose
* Pydantic models provide type-safety for tool arguments

Then, inspect the agent in `weather_agent.py`.

### Agent Setup

* The `Agent` class sets up a tool-calling agent
* The `role`, `goal`, and `instructions` guide the agent's behavior
* Tools are provided as a list for the agent to use

Run the weather agent:

```python
python weather_agent.py
```

**Expected output:** The agent will identify the locations and use the `get_weather` tool to fetch weather information for each city.

### Execution Flow

1. The agent receives a user query
2. The LLM determines which tool(s) to use based on the query
3. The agent executes the tool with appropriate arguments
4. The results are returned to the LLM to formulate a response
5. The final answer is provided to the user

## Working with Agent Memory

You can access and manage the agent's conversation history. Uncomment this code fragment in `weather_agent.py` and run the file again.

```python
# View the history after first interaction
print("Chat history after first interaction:")
print(AIAgent.chat_history)

# Second interaction (agent will remember the first one)
await AIAgent.run("How about in Seattle?")

# View updated history
print("Chat history after second interaction:")
print(AIAgent.chat_history)

# Reset memory
AIAgent.reset_memory()
print("Chat history after reset:")
print(AIAgent.chat_history)  # Should be empty now
```

**Expected output:** You will see the chat history log which will get reset and empty at the end.

The conversation history is a great way to debug your application quickly or for short-lived sessions. However, it will be lost if you restart your agent or the container crashes.

Next, we will explore how we can use Dapr to configure a state store that the agent can use to automatically save and load its history. The state store allows history to survive application or container restarts and it enables continuity between sessions.

### Persistent Agent Memory

Dapr Agents allows agents to retain long-term memory by providing automatic state management of the history. The state can be saved into a wide variety of [Dapr supported state stores](https://docs.dapr.io/reference/components-reference/supported-state-stores/). In short, Dapr manages the database setup, requiring only component configuration.

To configure persistent agent memory, follow these steps:

1. Set up the state store configuration. Here's an example of working with local Redis:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: historystore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

Create `historystore.yaml` file in the `./components` directory.

2. Now, let's enable Dapr memory by updating our weather agent.

First import the necessary dependencies:

```python
from dapr_agents.memory import ConversationDaprStateMemory
```

Then, update our agent:

```python
AIAgent = Agent(
    ...
    # Set memory store
    memory=ConversationDaprStateMemory(store_name="historystore", session_id="some-id")
)
```

3. Finally, run the Agent with Dapr

```bash
dapr run --app-id weatheragent --resources-path ./components -- python weather_agent.py
```

4. If you'd like to explore the chat history execute the following commands:

```bash
docker exec -it dapr_redis redis-cli
KEYS *
HGETALL weatheragent||some-id
```

We will explore the different Agent components and how to interact with them in more detail in the next part of the workshop.

## Available Agent Types

Dapr Agents provides two agent implementations, each designed for different use cases:

### 1. Agent

The default agent type, designed for tool execution and straightforward interactions. It receives your input, determines which tools to use, executes them directly, and provides the final answer. The reasoning process is mostly hidden from you, focusing instead on delivering concise responses.

### 2. DurableAgent

The DurableAgent class is a workflow-based agent that extends the standard Agent with Dapr Workflows for long-running, fault-tolerant, and durable execution. It provides persistent state management, automatic retry mechanisms, and deterministic execution across failures. We will explore how to create agent mesh using this agent in the next part of the workshop: [Durable Agent Mesh](../multi-agent-workflow/).

## Troubleshooting

1. **HuggingFace API Key**: Ensure your key is correctly set in the `.env` file
2. **Tool Execution Errors**: Check tool function implementations for exceptions
3. **Module Import Errors**: Verify that requirements are installed correctly

## Next Steps

After completing this assignment, move on to the [Durable Agent Mesh Workshop](../multi-agent-workflow/) to learn how to create Agent Mesh using Durable Agents.
