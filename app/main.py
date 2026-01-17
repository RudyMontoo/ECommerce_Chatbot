import streamlit as st
from router import router
from faq import faq_chain, ingest_faq_data
from sql import sql_chain
from pathlib import Path

# Advanced Custom CSS for Dark Theme
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Rows */
    .chat-row {
        display: flex;
        align-items: flex-end;
        margin-bottom: 20px;
        width: 100%;
    }
    .user-row {
        justify-content: flex-start;
    }
    .assistant-row {
        justify-content: flex-end;
    }

    /* Avatars */
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        flex-shrink: 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
    }
    .user-avatar {
        background-color: #2b313e; /* Darker gray for user avatar */
        margin-right: 12px;
        border: 1px solid #4a4a4a;
    }
    .assistant-avatar {
        background-color: #1e1e1e;
        margin-left: 12px;
        border: 1px solid #333;
    }

    /* Bubbles */
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        line-height: 1.5;
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        position: relative;
        animation: slideIn 0.3s ease-out;
    }
    
    .user-bubble {
        background-color: #262730; /* Dark gray for user bubble */
        color: #e0e0e0;
        border-bottom-left-radius: 4px;
        border: 1px solid #363636;
    }
    
    .assistant-bubble {
        /* Beautiful Blue Gradient for Dark Mode */
        background: linear-gradient(135deg, #006064 0%, #003366 100%);
        color: #ffffff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 15px rgba(0, 100, 255, 0.2);
    }

    /* Animation */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
</style>
""", unsafe_allow_html=True)

faqs_path = Path(__file__).parent / "resources" / "faq.csv"
ingest_faq_data(faqs_path)

def ask(query):
    # Clean query in case user added quotes
    query = query.strip('"').strip("'")
    route = router(query)
    print(f"DEBUG: Query='{query}' | Route='{route}' | Name='{getattr(route, 'name', 'N/A')}'")
    
    # Check if route is valid and has a name
    route_name = getattr(route, 'name', None)
    
    if route_name == "faq":
        return faq_chain(query)
    elif route_name == "sql":
        return sql_chain(query)
    elif route_name is not None:
         return f"Route **{route_name}** not implemented yet."
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

st.title("🛍️ ECommerce Assistant")
st.markdown("Ask me anything about products, return policies, or your orders!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-row user-row">
                <div class="avatar user-avatar">👤</div>
                <div class="chat-bubble user-bubble">{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-row assistant-row">
                <div class="chat-bubble assistant-bubble">{message["content"]}</div>
                <div class="avatar assistant-avatar">🤖</div>
            </div>
        """, unsafe_allow_html=True)

# Input
query = st.chat_input("Type your question here...")

if query:
    # 1. Display User Message Immediately
    st.markdown(f"""
        <div class="chat-row user-row">
            <div class="avatar user-avatar">👤</div>
            <div class="chat-bubble user-bubble">{query}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "user", "content": query})
    
    # 2. Get Response
    response = ask(query)
    
    # 3. Display Assistant Message
    st.markdown(f"""
        <div class="chat-row assistant-row">
            <div class="chat-bubble assistant-bubble">{response}</div>
            <div class="avatar assistant-avatar">🤖</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
