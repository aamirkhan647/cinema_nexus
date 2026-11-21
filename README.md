# CinemaNexus

**CinemaNexus** is an enterprise-grade multi-agent movie intelligence system built with the **Google Agent Development Kit (ADK)** and the **Google GenAI SDK** powered by `gemini-3-flash-preview`. It coordinates specialized sub-agents to deliver live film reviews, context-aware recommendations, and personal watchlist curation, secured by multi-layered guardrails.

---

## Architecture Overview

```
                      ┌───────────────────────────┐
                      │    CinemaNexusDirector    │ (Root Orchestrator)
                      │  [before_model_callback]  │ -> Prompt Injection Defense
                      │  [after_model_callback]   │ -> PII Redaction
                      └─────────────┬─────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌──────────────┐            ┌─────────────────┐          ┌────────────────┐
│ CriticAgent  │            │RecommenderAgent │          │ WatchlistAgent │
├──────────────┤            ├─────────────────┤          ├────────────────┤
│ MCP Web      │            │ MCP Web Fetch   │          │ Custom Tool:   │
│ Fetch Tool   │            │ State-aware:    │          │ manage_        │
│ output_key:  │            │ {user_watchlist}│          │ watchlist      │
│ 'last_review'│            └─────────────────┘          │ [Tool Guard]   │
└──────────────┘                                         └────────────────┘
```

### Agent Roles

- **`CinemaNexusDirector` (Root Orchestrator)**: Manages intent delegation, introduces the service, enforces a system-wide `global_instruction` (formatting standards and movie/TV scope enforcement), and applies pipeline guardrails.
- **`CriticAgent`**: Gathers and synthesizes live critical reception, box office data, and ratings (IMDb, Rotten Tomatoes) using web content fetched via MCP. Results are persisted to session state under `last_review`.
- **`RecommenderAgent`**: Generates personalized movie recommendations and comparisons. Leverages dynamic ADK prompt templating (`{user_watchlist}`) to avoid suggesting movies already saved in the user's list.
- **`WatchlistAgent`**: Manages personal watchlists (viewing, adding, removing) with deterministic parameters (`temperature=0.1`) and tool-level validation.

---

## Defense-in-Depth Safety Guardrails

CinemaNexus implements three independent layers of security and validation:

1. **Input Guardrail (`before_model_callback`)**: Intercepts requests before LLM inference to block prompt injection, jailbreak attempts, or unauthorized instruction overrides.
2. **Output Guardrail (`after_model_callback`)**: Inspects model responses before returning them to the user, redacting Personally Identifiable Information (PII) including emails, phone numbers, and Social Security Numbers.
3. **Tool Guardrail (`before_tool_callback`)**: Pre-validates parameters sent to `manage_watchlist`, trimming inputs, enforcing a title length limit ($\le 200$ chars), and capping the user's watchlist size at 50 items.

---

## Project Structure

```
cinema_nexus/
├── agents/                   # Modular agent definitions
│   ├── __init__.py           # Exports domain agents and root orchestrator
│   ├── critic.py             # CriticAgent: web fetch & synthesis
│   ├── director.py           # CinemaNexusDirector: root orchestrator
│   ├── recommender.py        # RecommenderAgent: state-aware discovery
│   └── watchlist.py          # WatchlistAgent: watchlist curation
├── schemas/                  # Structured data models & schemas
│   ├── __init__.py           # Exports schemas and enums
│   ├── actions.py            # WatchlistAction enum
│   └── payloads.py           # WatchlistResult, GuardrailResult schemas
├── safety/                   # Multi-layered security & validation
│   ├── __init__.py           # Exports guardrail callbacks and filters
│   ├── callbacks.py          # before_model, after_model, before_tool callbacks
│   └── filters.py            # Injection patterns, PII regex, limits
├── tools/                    # Tool integrations & operations
│   ├── __init__.py           # Exports tools and MCP toolsets
│   ├── mcp_toolsets.py       # MCP fetch client definition
│   └── watchlist_ops.py      # Stateful watchlist tool logic
├── agent.py                  # Top-level ADK entry point (root_agent export)
├── config.py                 # Central configuration (models, timeouts, limits)
├── run.py                    # Direct CLI runner (Windows compatible)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
└── README.md                 # System documentation
```

---

## Key Features & Technologies

- **Google Agent Development Kit (ADK)**: Hierarchical agent delegation and lifecycle callbacks.
- **Gemini 3 Flash (`gemini-3-flash-preview`)**: High-speed, high-reasoning multimodal language model.
- **Google Cloud Vertex AI & ADC**: Native enterprise authentication using Application Default Credentials.
- **Model Context Protocol (MCP)**: Dynamic tool integration using `mcp-server-fetch` via `uvx` for real-time web data extraction.
- **Session State Persistence (`ToolContext.state`)**: Cross-agent state sharing for watchlist items and review history.
- **Pydantic Validation**: Structured typing for tool inputs, tool execution results, and safety inspection reports.

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js / uvx**: Required to run the MCP fetch tool server (`uvx mcp-server-fetch`). Verify with:
  ```bash
  uvx --version
  ```
- **Google Cloud SDK (`gcloud` CLI)**: Configured and authenticated.

### Authentication & Setup

1. **Authenticate to Google Cloud** via Application Default Credentials (ADC):
   ```cmd
   gcloud auth application-default login
   ```

2. **Navigate to the project directory:**
   ```cmd
   cd cinema_nexus
   ```

3. **Create and activate a virtual environment:**
   ```cmd
   python -m venv .venv
   # Windows (Command Prompt):
   .venv\Scripts\activate.bat
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

4. **Install required dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   ```cmd
   # Windows:
   copy .env.example .env
   # macOS/Linux:
   cp .env.example .env
   ```
   Edit `.env` to specify your Google Cloud project and region:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   ```

---

## Running the Application

The system can be run from the command line using either the included runner script (`python run.py`) or the **ADK CLI** (`adk`).

### Option 1: Direct Runner (Recommended on Windows)

The project includes `run.py` which launches the interactive CLI session directly while bypassing Windows symlink privilege restrictions:

```cmd
python run.py
```
To save the session on exit:
```cmd
python run.py --save_session
```

---

### Option 2: Interactive Terminal CLI (`adk run`)

Run an interactive chat session using the ADK CLI:

```cmd
adk run .
```

---

### Option 3: Browser Web UI (`adk web`)

ADK provides a built-in FastAPI web server and GUI for interacting with agents:

```cmd
adk web ..
```
Then navigate to:
```
http://127.0.0.1:8000
```

---

## Example Queries

Once running, try prompts that route to different sub-agents:

- **CriticAgent**:
  - *"Review Inception"*
  - *"What's the Rotten Tomatoes rating and critical consensus for Arrival?"*
- **RecommenderAgent**:
  - *"What should I watch next if I like Life of Pi?"*
  - *"Compare Interstellar vs Arrival and recommend which one to watch tonight."*
- **WatchlistAgent**:
  - *"Add Encanto to my watchlist"*
  - *"Show my current watchlist"*
  - *"Remove Inception from my watchlist"*


## Example Run

```
[user]: Suggest me a movie if I liked "Bugs life" previously
auth_config or auth_config.auth_scheme is missing. Will skip authentication.Using FunctionTool instead if authentication is not required.
auth_config or auth_config.auth_scheme is missing. Will skip authentication.Using FunctionTool instead if authentication is not required.
[RecommenderAgent]: ## If You Liked A Bug's Life, Try These

| # | Movie | Why |
|---|-------|-----|
| 1 | **Antz (1998)** | Released the same year as *A Bug's Life*, this film offers a slightly more mature take on ant colony life, focusing on an individualist ant named Z who rebels against a militaristic general. |
| 2 | **The Ant Bully (2006)** | This film flips the perspective by shrinking a human boy down to ant size, forcing him to live and work within the colony he once tormented. |
| 3 | **Bee Movie (2007)** | Another insect-centric comedy that explores the "hidden world" of bugs, following a bee who discovers humans have been stealing honey and decides to sue the human race. |

**Top pick:** **Antz (1998)** - It is the most natural companion to *A Bug's Life*. While it shares the same setting, it features a unique visual style and a star-studded voice cast (including Woody Allen and Sylvester Stallone), focusing on themes of individuality versus the hive mind.
[user]: 
```