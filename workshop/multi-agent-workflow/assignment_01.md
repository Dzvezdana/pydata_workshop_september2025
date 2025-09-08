# Multi-Agent Event-Driven Workflows

For this workshop, you will build a Fellowship of the Ring quest planning system. This system simulates how different members of the fellowship coordinate to plan their journey to Mount Doom, each contributing based on their unique expertise and personality.

After finishing this workshop you will understand how to:

* create and configure AI agents' personality and behavior
* configure durable AI agents using Dapr component configuration (state stores, pub/sub)
* orchestrate multiple agents

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

2. Create a `.env` file for your API keys in `workshop/multi-agent-workflow/`

```env
export HUGGINGFACE_API_KEY=your_api_key_here >> .env
```

Make sure Dapr is initialized on your system:

```
dapr init
```

## Assignment 1. Define Agents Characteristics, Personality, and Capabilities

This assignment demonstrates how to define the agents' characteristics, personality, and capabilities.

### Exercise 1: Explore Agent Behavior

In a multi-agent system, each agent is specialized for a particular role. Each agent has its own service implementation that defines its unique characteristics, personality, and capabilities. Use the Editor window to examine the Hobbit agent implementation in the `services/hobbit/app.py` file:

```python
from dapr_agents import DurableAgent
from dotenv import load_dotenv
import asyncio
import logging


async def main():
    try:
        hobbit_service = DurableAgent(
            name="Frodo",
            role="Hobbit",
            goal="Carry the One Ring to Mount Doom, resisting its corruptive power while navigating danger and uncertainty.",
            instructions=[
                "Speak like Frodo, with humility, determination, and a growing sense of resolve.",
                "Endure hardships and temptations, staying true to the mission even when faced with doubt.",
                "Seek guidance and trust allies, but bear the ultimate burden alone when necessary.",
                "Move carefully through enemy-infested lands, avoiding unnecessary risks.",
                "Respond concisely, accurately, and relevantly, ensuring clarity and strict alignment with the task.",
            ],
            ...
        )

        await hobbit_service.start()
    except Exception as e:
        print(f"Error starting service: {e}")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
```

You'll notice how the "Frodo" agent is defined with specific personality traits, goals, and instructions that shape its behavior. The agent is configured with:

* A clear role and name
* A specific goal that drives its actions
* Detailed instructions that define its personality and response style

Next, use the Editor window to explore the wizard agent in the `services/wizard/app.py` file. Compare how "Gandalf" differs from "Frodo" - you'll see different goals, instructions, and personality traits that make this agent behave as a wise advisor rather than a determined ring-bearer.

Finally, examine the elf agent implementation in the `services/elf/app.py` file. Notice how "Legolas" has yet another distinct personality and set of capabilities, emphasizing keen observation, precision, and scouting abilities.

Each agent follows the same structural pattern but with unique characteristics that make them suitable for different aspects of problem-solving. This specialization allows the multi-agent system to tackle complex tasks by leveraging the diverse strengths of each participant.

### Exercise 2: Observe Agent Interactions

#### CLI

Start all services using the Dapr CLI:

<!-- STEP
name: Run text completion example
match_order: none
expected_stdout_lines:
  - "Workflow started successfully!"
  - "user:"
  - "How to get to Mordor? We all need to help!"
  - "assistant:"
  - "user:"
  - "assistant:"
  - "workflow completed with status 'ORCHESTRATION_STATUS_COMPLETED' workflowName 'RandomWorkflow'"
timeout_seconds: 120
output_match_mode: substring
background: false
sleep: 5
-->
```bash
dapr run -f dapr-random.yaml 
```
<!-- END_STEP -->

**Expected output:** The agents will engage in a conversation about getting to Mordor, with different agents contributing based on their character. Observe this in the logs.

Open a new Terminal window and list all available services:

```bash
dapr list
```

**Expected output:** Returns a list of all available services and their ports.

#### Conversation log

Use the Editor window to open the `services/hobbit/Frodo_state.json` file and inspect its content. This file is a conversation log from a Dapr Agents run, capturing interactions between agents like Frodo, Legolas, Gandalf and an orchestrator (more on the orchestrator in Assignment 3). It records inputs, outputs, message history, timestamps, and workflow metadata for debugging, auditing, or replaying multi-agent dialogues.

#### Dapr Dashboard

Open a new terminal and start the Dapr Dashboard by running:

```
dapr dashboard
```

You can view components, configurations, and service details at http://localhost:8080/

#### Zipkin Tracing

Zipkin is a distributed tracing system. In the context of Dapr (and microservices in general), it’s used to collect and visualize trace data across multiple services so you can understand how requests flow through your system.
You can access it here http://localhost:9411/zipkin/

### Monitoring and Observability Summary
1. **Console Logs**: Monitor real-time workflow execution and agent interactions
2. **Dapr Dashboard**: View components, configurations and service details at http://localhost:8080/
3. **Zipkin Tracing**: Access distributed tracing at http://localhost:9411/zipkin/
4. **Dapr Metrics**: Dapr supports monitoring agent performance metrics via (ex: HobbitApp) http://localhost:6001/metrics. This requires setting up Prometheus and is outside the scope of this workshop.

## Exercise 3: Add Additional Lord of the Rings Characters

Let's add an extra agent to the mix! Our current characters are hobbit, wizard and elf.

Try to add more Lord of the Rings characters as services, for example you could add an eagle, dwarf and/or ranger.

To do this:

1. Add a new folder in `services` and copy the contents of `app.py`.
2. Adjust the `name`, `role`, `goal` and the `instructions`. Do not adjust the other fields.
3. Register your newly created service in `dapr-random.yaml`.
4. Rerun your app.

If you are stuck, you can take a look at the [solutions folder](../../solutions/).

## When to Use Multi-Agent Systems

Multi-agent systems are particularly well-suited for:

* Complex Problem Solving: Tasks requiring multiple types of expertise
* Creative Collaboration: Generating ideas from diverse perspectives
* Role-Playing Scenarios: Simulating interactions between different characters
* Debate and Deliberation: Presenting multiple viewpoints on a topic
* Distributed Processing: Breaking down large tasks into parallel operations

By leveraging multiple specialized agents, you can create AI systems that tackle problems too complex for a single agent to handle effectively.

## Troubleshooting

* API Key Issues: If you see an authentication error, verify your HuggingFace API key is set,
* Python Version: If you encounter compatibility issues, make sure you're using Python 3.10+
* Import Errors: If you see module not found errors, verify that pip install -r requirements.txt completed successfully
* Workflows Errors: Run: `docker exec dapr_redis redis-cli FLUSHALL && docker restart dapr_redis`

## Next assignment

Ensure all running processes are stopped before proceeding to the next assignment. Let's move on to the next challenge where you'll learn how to configure durability in Agents.
