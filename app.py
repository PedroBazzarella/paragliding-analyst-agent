import streamlit as st
from datetime import datetime
from langgraph.checkpoint.memory import InMemorySaver
from agent.core import build_agent

# Page Config
st.set_page_config(
    page_title="Climate Analysis Agent",
    page_icon="🪂",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize Session
if "checkpointer" not in st.session_state:
    st.session_state.checkpointer = InMemorySaver()

if "agent" not in st.session_state:
    st.session_state.agent = build_agent(st.session_state.checkpointer)

agent = st.session_state.agent

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Each log {prompt, response, timestamp}
 
 
def extract_message(raw):
    """Extract content string from a raw LangChain message repr or object."""
    if hasattr(raw, "content"):
        return raw.content
    s = str(raw)
    # Pull out content='...' safely
    import re
    m = re.search(r"content='(.*?)'(?:,|\s+additional_kwargs)", s, re.DOTALL)
    if m:
        return m.group(1)
    return s
 
 
def extract_tool_name(raw):
    """Try to get the tool name from a model AIMessage that has tool_calls."""
    if hasattr(raw, "tool_calls") and raw.tool_calls:
        return raw.tool_calls[0].get("name", "unknown tool")
    s = str(raw)
    import re
    m = re.search(r"'name':\s*'([^']+)'", s)
    if m:
        return m.group(1)
    return None
 
 
def extract_tool_result(raw):
    """Get the content of a ToolMessage."""
    if hasattr(raw, "content"):
        return raw.content
    s = str(raw)
    import re
    m = re.search(r"content='(.*?)'(?:,|\s+name=)", s, re.DOTALL)
    if m:
        result = m.group(1)
        # Decode common escape sequences
        result = result.encode().decode("unicode_escape", errors="replace")
        return result
    return s

# Agent
def call_agent(prompt: str):
    final_response = ""
 
    # Reading prompt
    with st.status("🔍 Reading your prompt…", expanded=False) as status:
        pending_final = None
 
        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": prompt}]},
            {"configurable": {"thread_id": "1"}},
        ):
            # Model chunk
            if "model" in chunk:
                messages = chunk["model"].get("messages", [])
                for msg in messages:
                    tool_name = extract_tool_name(msg)
                    content = extract_message(msg)
 
                    if tool_name:
                        # Tool call
                        status.update(
                            label=f"🔧 Calling tool: `{tool_name}`",
                            expanded=False,
                        )
                    elif content:
                        # Final response
                        pending_final = content
 
            # Tools chunk
            elif "tools" in chunk:
                messages = chunk["tools"].get("messages", [])
                for msg in messages:
                    result = extract_tool_result(msg)
                    # Tool result
                    status.update(
                        label="📊 Tool returned a result",
                        expanded=False,
                    )
                    
        status.update(label="✅ Agent finished processing", state="complete", expanded=False)
 
    # Final response
    if pending_final:
        st.write(pending_final)
        final_response = pending_final
 
    return final_response

# Save chat history
def save_chat(prompt: str, response: str, timestamp: datetime):
    st.session_state.chat_history.append({
        "prompt": prompt,
        "response": response,
        "timestamp": timestamp
    })

# Append chat messages
def append_prompt(prompt: str, timestamp: datetime):
    with st.chat_message("user", avatar="🧐"):
        st.markdown(
            f"<p style='font-size: 12px; color: gray;'>{timestamp.strftime('%H:%M')}</p>",
            unsafe_allow_html=True
        )
        st.write(prompt)

def append_response(prompt: str):
    with st.chat_message("assistant", avatar="🪂"):
        response = call_agent(prompt)
    return response

# Sidebar
with st.sidebar:
    st.markdown("# Chats")
    st.divider()

    st.markdown(
        "<p>Nothing here yet.</p>",
        unsafe_allow_html=True
    )

# Header
st.title("🪂 Climate Analysis Agent", anchor=False)
st.markdown("Generate climate analysis reports using natural language.")
st.divider()

# Chat
with st.container():
    for log in st.session_state.chat_history:
        append_prompt(log["prompt"], log["timestamp"])
        with st.chat_message("assistant", avatar="🪂"):
            st.write(log["response"])

# Input
prompt = st.chat_input("Is the weather in Montes Claros good for paragliding?")
if prompt:
    now = datetime.now()
    append_prompt(prompt, now)
    response = append_response(prompt)
    save_chat(prompt, response, now)