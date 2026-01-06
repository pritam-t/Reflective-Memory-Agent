# Reflective Memory Agent

A **self-evolving AI agent** with **reflection-based memory consolidation**.  
Instead of storing every conversation, this agent reflects, evaluates, and selectively remembers only meaningful insights — much like **human memory**.

---

## 🚀 Key Features

- **Reflection-Based Memory:** The agent analyzes each interaction to decide what’s worth remembering.  
- **Long-Term Vector Memory:** Uses **Qdrant** to store user-specific memories for persistent knowledge.  
- **Selective Consolidation:** Only high-importance facts, preferences, or insights are saved.  
- **User-Specific Identity:** Remembers key preferences (programming languages, styles, etc.).  
- **Agent Behavior Evolution:** Over time, the agent adapts its responses based on stored memories.  
- **Hybrid / Local LLM:** Designed to run on local models, but currently uses OpenAI API for reflection quality.

---

## 🧩 System Architecture

![Architecture Diagram](diagrams/architecture.png)

- **Reflection Agent**: Analyzes conversation, scores importance, decides what to store.  
- **Memory Importance Scoring**: Ensures only high-value memories are persisted.  
- **Personality/Behavior Update**: Optional module to influence future responses.


---

## 💻 Installation

1. **Clone the repository**
```bash
git clone https://github.com/pritam-t/Reflective-Memory-Agent.git
cd Reflective-Memory-Agent
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create a .env file
OPENAI_API_KEY=your_openai_api_key_here
Run Qdrant with persistent storage
```

5. **powershell**
```bash
docker run -d `
  --name qdrant `
  -p 6333:6333 `
  -v qdrant_data:/qdrant/storage `
  qdrant/qdrant
```

5. **⚡ Usage**
```bash
python agent.py
```

Then type input in the console. Example:

```ruby
Copy code
>> I mainly use Java for robotics programming.
>> What programming language do I prefer?
The agent will reflect, decide what to store, and retrieve relevant memories for responses.
```

Memory persists across agent restarts if Qdrant container uses a persistent volume.


📂 Repository Structure
```bash
Copy code
Reflective-Memory-Agent/\n
├─ agent.py           # Main agent loop
├─ requirements.txt   # Dependencies
├─ .env               # API keys (not pushed)
├─ README.md          # Documentation
├─ .gitignore
└─ diagrams/          # Optional architecture diagram
🏷️ License
```

# MIT License – free to use, modify, and experiment with.