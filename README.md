# Dapr in Action: Collaborative Multi-Agent Workflow

### Presentation: [Slides](./workshop/dapr_pydata_2025.pdf)

## Workshop description

Welcome to the workshop on building AI Agents with Dapr!

[Dapr](https://github.com/dapr/dapr) is a powerful open-source runtime that simplifies building distributed applications. During this session, you'll get up to speed on Dapr's fundamentals and gain practical experience creating AI agents using [dapr-agents](https://github.com/dapr/dapr-agents).

## Introductory Workshop Requirements 

First clone the repo:

```bash
git clone https://github.com/Dzvezdana/pydata_workshop_september2025
cd pydata_workshop_september2025/
```

## Usage

Make sure you have Python 3.10+ installed.

Set up a virtual environment using virtualenv:

```
# Install virtualenv package (typically pre-installed)
pip install virtualenv

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment (command might differ per OS)
source ./.venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dapr

Install Dapr CLI and Docker Desktop:

* [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
* [Docker Desktop](https://docs.docker.com/desktop/)

Check if Dapr was installed correctly:

```
dapr -h
```

Then, initialize Dapr:

```
dapr init
```
       
### API Keys

API keys can be accessed via this [privatebin](TODO). The password will be shared during the workshop.

The keys will only be available during the workshop. If you want to follow the workshop after, please generate read-only HuggingFace API key yourself first at https://huggingface.co/.

If you need a quick recap on agents and tools, navigate to `workshop/intro-to-agents/`:

```env
cd workshop/intro-to-agents/
export HUGGINGFACE_API_KEY=your_api_key_here >> .env
```

Open `[optional] assignment_01.md` and start the workshop.

After you are done with this assignment, create a `.env` file in the `workshop/multi-agent-workflow/` directory with your API keys:

```env
cd workshop/multi-agent-workflow/
export HUGGINGFACE_API_KEY=your_api_key_here >> .env
```

Open `assignment_01.md` and start the workshop.

## Credits

This workshop was set up by Dana Arsovska ([Git](https://github.com/Dzvezdana), [LinkedIn](https://www.linkedin.com/in/dana-arsovska/)) and Marc Duiker ([web site](https://marcduiker.dev/)).

All code samples shown in this workshop are available in the [Dapr Agents repository](https://github.com/dapr/dapr-agents/tree/main) in the quickstarts folder. Give this repo a star and clone it locally to use it as reference material for building your next Dapr Agents project.

You can also check out the free [Dapr Agents Course at Dapr University](https://www.diagrid.io/dapr-university).

If you are doing this workshop at home and have any questions, join [Dapr's Community Discord channel](https://dapr.io/community/).

Thank you for joining and participating in our workshop! ✨🎉
