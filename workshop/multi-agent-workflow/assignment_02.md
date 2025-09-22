# Multi-Agent Event-Driven Workflows

## Assignment 2. Build Stateful and Resilient Agents

In this challenge, you will learn how to create durable AI agents that can survive failures and maintain state.

### Why Use DurableAgent?

The DurableAgent is Dapr Agents' most powerful and resilient agent type, designed for production-level AI applications. The DurableAgent:

* Implements the Workflow Pattern: Uses Dapr's workflow engine to execute tasks in a durable, recoverable manner
* Preserves State Across Failures: Stores all conversation state and execution progress in persistent storage
* Manages Complex Tool Interactions: Orchestrates tool calls with proper error handling and retry logic
* Supports Multi-Agent Communication: Can broadcast messages to other agents and receive responses
* Exposes Service APIs: Provides REST endpoints to trigger workflows and check their status

This makes the DurableAgent ideal for mission-critical applications that need to remain functional even when facing system failures, network issues, or process restarts.

### Exercise 1: Dapr Components Deep Dive

Let's explore the key components that enable durability using the Hobbit agent implementation in the `services/hobbit/app.py` file.

```python
from dapr_agents import DurableAgent
from dotenv import load_dotenv
import asyncio
import logging


async def main():
    try:
        hobbit_service = DurableAgent(
            name="Frodo",
            ...
          message_bus_name="messagepubsub",
          state_store_name="workflowstatestore",
          state_key="workflow_state",
          agents_registry_store_name="agentstatestore",
          agents_registry_key="agents_registry",
          broadcast_topic_name="beacon_channel",
        )

        await hobbit_service.start()
    except Exception as e:
        print(f"Error starting service: {e}")


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
```

#### Message Bus

`message_bus_name` is used to integrate with Dapr pub/sub for asynchronous communication between agents and services.

```python
message_bus_name="messagepubsub",
```

In `components/pubsub.yaml` we configure [Redis Streams](https://docs.dapr.io/reference/components-reference/supported-pubsub/setup-redis-pubsub/) as the backend transport mechanism for publishing and subscribing to messages.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: messagepubsub
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

Finally, `broadcast_topic_name` is the pub/sub topic where an agent publishes messages that all subscribed agents can receive.

#### State Stores for Workflow Orchestration

`state_store_name` and `state_key` configure where the agent stores its execution state for workflows. This enables the agent to resume execution from where it left off if interrupted.

```python
state_store_name="workflowstatestore",
state_key="workflow_state",
```

In `components/workflowstatestore.yaml` we configure [Redis](https://docs.dapr.io/reference/components-reference/supported-state-stores/setup-redis/) to provide state persistence for the agents.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: workflowstatestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```

#### Agent Registry

The agent registry stores metadata about available agents, their capabilities, and state. This enables service discovery and coordination in multi-agent systems.

```python
agents_registry_store_name="registrystatestore",
agents_registry_key="agents_registry",
```

In `components/agentstate.yaml` Redis is again used as a state store to store agent metadata and registration info.

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: agentstatestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: keyPrefix
    value: none
  - name: actorStateStore
    value: "true"
```

#### Service Exposure

`hobbit_service.start()` exposes the agent as a REST service, allowing other systems to interact with it through standard HTTP requests.

3. Run the Durable Agent

```bash
dapr run -f dapr-random.yaml 
```

This command:

    1. Starts Dapr with the specified application ID
    2. Configures the port for the REST API
    3. Sets the path to the component configurations
    4. Launches the agent application


### Exercise 2: Inspect Agent State in Redis

Let's examine how state is stored:

```bash
# Connect to Redis and explore keys
docker exec -it dapr_redis redis-cli
> KEYS *
> HGETALL agents_registry
> HGETALL WizardApp||workflow_state
```

**Expected output:** You should see keys related to workflow state, agent registry, and pub/sub messages.

### Exercise 3: Interact with the Durable Agent

Unlike simpler agents, durable agents provide REST APIs for interaction. Here's how to use them:

#### Start a Workflow

Open a new Terminal window and list all available services again:

```bash
dapr list
```

Run this command in the **cURL** window to start a new workflow:

```bash
INSTANCEID=$(curl -s -X POST http://localhost:8004/start-workflow \
  -H "Content-Type: application/json" \
  -d '{"task": "We need to discuss our route to Mordor. What do you think?"}' | \
  grep -o '"workflow_instance_id":"[^"]*"' | \
  sed 's/"workflow_instance_id":"//;s/"//g' | \
  tr -d '\r\n')
```

This initiates a new workflow for finding a route. You will receive a workflow ID in response.

#### Check the Workflow Status

Run this command in the **cURL** window to check the status of the workflow. First replace port name with the HTTP Port of the WorkflowApp shown when running `dapr list`.

```bash
curl -i -X GET http://localhost:<PORT_NAME>/v1.0/workflows/WorkflowApp/$INSTANCEID 
```

This allows you to track the progress of long-running tasks.

### Exercise 4: Test State Recovery After Failure

1. Open the Dapr Dashboard at http://localhost:8080
2. Go to the "Applications" tab
3. Find the agent you want to stop (e.g., "HobbitApp"). Stop the agent.

**Expected behavior:** The agent should resume from where it left off, demonstrating durability.

### [Optional] Exercise 5: Add ConversationDaprStateMemory

`ConversationDaprStateMemory` configures the agent to store its conversation history in a Dapr state store, enabling it to remember context across sessions and survive restarts. In this optional exercise, try to enable `ConversationDaprStateMemory` for our `DurableAgents`.

**Hints**:

* Take a look at the [docs](https://v1-16.docs.dapr.io/developing-applications/dapr-agents/dapr-agents-core-concepts/).
* Don't forget to add a new component in the `components` folder.

## Next assignment

You've now learned about how to define durable AI agents that can survive failures and maintain state across sessions. Let's move on to the next challenge where you will learn about different types of workflow orchestration. Make sure you stop all running processes before proceeding to the next assignment.
