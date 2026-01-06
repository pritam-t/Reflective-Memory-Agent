from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
import os
import json

# -----------------------
# Environment
# -----------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------
# Memory Configuration
# -----------------------
config = {
    "version": "0.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4.1-mini"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "reflective_memory_agent"
        }
    }
}

memory = Memory.from_config(config)

USER_ID = "pritam_123"

# -----------------------
# Reflection Agent
# -----------------------
def reflect_and_score(user_msg, assistant_msg):
    """
    Returns:
    {
        "summary": str,
        "importance": int (0-10),
        "store": bool
    }
    """

    prompt = f"""
You are a reflection agent.

Conversation:
User: {user_msg}
Assistant: {assistant_msg}

Decide:
1. Is there a stable user preference, identity signal, or long-term useful fact?
2. Summarize it in ONE sentence.
3. Give an importance score (0-10).

Rules:
- Preferences (language, tools, style) are ALWAYS important (>=6).
- Store only if importance >=5.

Respond in JSON:
{{
  "summary": "...",
  "importance": 0-10,
  "store": true/false
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)

# -----------------------
# Main Agent Loop
# -----------------------
while True:
    user_input = input("\n>> ")

    # 1️⃣ Retrieve memory
    retrieved = memory.search(
        user_id=USER_ID,
        query=user_input,
        limit = 5
    )

    memories = [
        f"- {m['memory']}"
        for m in retrieved.get("results", [])
    ]

    memory_context = "\n".join(memories) if memories else "No relevant memories."

    # 2️⃣ Generate response
    system_prompt = f"""
You are an AI assistant with long-term memory.

Relevant memories:
{memory_context}

Use them ONLY if helpful.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    assistant_reply = response.choices[0].message.content
    print("\nAssistant:", assistant_reply)

    # 3️⃣ Reflection + scoring
    reflection = reflect_and_score(user_input, assistant_reply)

    # print(f"\n🪞 Reflection: {reflection}")

    # 4️⃣ Memory consolidation
    if reflection["store"]:
        memory.add(
            user_id=USER_ID,
            messages=[
                {
                    "role": "system",
                    "content": reflection["summary"]
                }
            ]
        )
        print("🧠 Memory stored.")
    else:
        print("🧠 Nothing worth remembering.")
