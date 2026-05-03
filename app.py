import streamlit as st
import requests
import json

# ── CONFIG ────────────────────────────────────────────────────────────────────
N8N_WEBHOOK = "http://localhost:5678/webhook/c0d5190d-34d8-4fc0-8d94-1df6a3ac094a"
TIMEOUT     = 60

st.set_page_config(
    page_title="ARIA — Aleem's Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #f5f6ff !important;
    font-family: 'Inter', sans-serif !important;
    color: #0f0f1a !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    padding: 0 0 140px 0 !important;
    max-width: 860px !important;
}

/* ── NAV ── */
.aria-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    height: 62px;
    background: #ffffff;
    border-bottom: 1px solid #e8e8f5;
    margin-bottom: 0;
}
.aria-logo {
    font-size: 1.25rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    color: #0f0f1a;
}
.aria-logo span { color: #6366f1; }
.aria-nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
}
.online-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 700;
    color: #16a34a;
    letter-spacing: 0.02em;
}
.online-dot {
    width: 6px; height: 6px;
    background: #22c55e;
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
.user-chip {
    display: flex;
    align-items: center;
    gap: 9px;
    font-size: 13px;
    font-weight: 600;
    color: #374151;
}
.user-avatar {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: #fff;
    font-size: 13px;
    font-weight: 700;
}

/* ── HERO ── */
.aria-hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #9333ea 100%);
    padding: 52px 32px 60px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 36px;
}
.aria-hero::before {
    content: '';
    position: absolute; inset: 0;
    background-image: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.06) 0%, transparent 50%),
                      radial-gradient(circle at 80% 20%, rgba(255,255,255,0.04) 0%, transparent 40%);
}
.hero-greet {
    font-size: 12px; font-weight: 600;
    color: rgba(255,255,255,0.6);
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 10px; position: relative;
}
.aria-hero h1 {
    font-size: clamp(2rem, 6vw, 3.6rem);
    font-weight: 900; letter-spacing: -0.04em;
    color: #fff; line-height: 1.05;
    margin-bottom: 14px; position: relative;
}
.aria-hero h1 span {
    background: linear-gradient(90deg, #fde68a, #fbbf24);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.aria-hero p {
    font-size: 0.97rem; font-weight: 400;
    color: rgba(255,255,255,0.68);
    max-width: 420px; margin: 0 auto;
    line-height: 1.75; position: relative;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase;
    color: #9ca3af;
    margin-bottom: 16px; padding: 0 2px;
}

/* ── CAPABILITIES ── */
.caps-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 40px;
}
.cap-card {
    background: #fff;
    border: 1px solid #e8e8f5;
    border-radius: 14px;
    padding: 18px 16px;
    display: flex; align-items: flex-start; gap: 13px;
    transition: all 0.22s ease;
}
.cap-card:hover {
    border-color: #a5b4fc;
    box-shadow: 0 4px 20px rgba(99,102,241,0.09);
    transform: translateY(-2px);
}
.cap-icon {
    width: 40px; height: 40px;
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.ic-1 { background: #ede9fe; }
.ic-2 { background: #dbeafe; }
.ic-3 { background: #dcfce7; }
.ic-4 { background: #ffedd5; }
.ic-5 { background: #fce7f3; }
.ic-6 { background: #fef9c3; }

.cap-info h4 {
    font-size: 0.82rem; font-weight: 700;
    color: #111827; margin-bottom: 3px;
}
.cap-info p {
    font-size: 0.73rem; color: #9ca3af; line-height: 1.5;
}

/* ── CHAT DIVIDER ── */
.chat-divider {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 20px;
}
.div-line { flex: 1; height: 1px; background: #e8e8f5; }
.div-label {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #9ca3af;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 3px 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {
    background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
    border: none !important;
    border-radius: 18px 4px 18px 18px !important;
    padding: 11px 16px !important;
    color: #fff !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    background: #ffffff !important;
    border: 1px solid #e8e8f5 !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 11px 16px !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-radius: 50% !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: #fff !important;
    border: 1px solid #e8e8f5 !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}

/* ── CHAT INPUT ── */
[data-testid="stBottom"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 860px !important;
    padding: 12px 24px 22px !important;
    background: linear-gradient(to top, #f5f6ff 70%, transparent) !important;
    z-index: 999 !important;
}
[data-testid="stChatInput"] {
    background: #fff !important;
    border: 1.5px solid #e0e0f5 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.08) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 4px 28px rgba(99,102,241,0.16) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #0f0f1a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #c4c4d4 !important;
}

/* ── ERROR BOX ── */
.error-box {
    background: #fff5f5;
    border: 1px solid #fecaca;
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 0.85rem;
    color: #b91c1c;
    margin: 8px 0;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #ddd8f8; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── HELPER: CALL N8N ──────────────────────────────────────────────────────────
def call_aria(message: str) -> str:
    """Send message to n8n and parse response robustly."""
    try:
        res = requests.post(
            N8N_WEBHOOK,
            json={"message": message, "chatInput": message},
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT,
        )
        res.raise_for_status()

        # Handle empty response
        raw = res.text.strip()
        if not raw:
            return "⚠️ ARIA received an empty response from the backend. Make sure the n8n workflow is active and published."

        data = res.json()

        # n8n returns list
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            return (
                item.get("output")
                or item.get("text")
                or item.get("message")
                or item.get("response")
                or item.get("answer")
                or str(item)
            )

        # n8n returns dict
        if isinstance(data, dict):
            return (
                data.get("output")
                or data.get("text")
                or data.get("message")
                or data.get("response")
                or data.get("answer")
                or str(data)
            )

        return str(data)

    except requests.exceptions.ConnectionError:
        return "⚠️ Cannot connect to n8n. Make sure n8n is running on localhost:5678."
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. n8n took too long to respond (>60s)."
    except requests.exceptions.HTTPError as e:
        return f"⚠️ n8n returned an error: {e.response.status_code} — {e.response.text[:200]}"
    except json.JSONDecodeError:
        return f"⚠️ Could not parse n8n response. Raw output: {res.text[:300]}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"


# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aria-nav">
    <div class="aria-logo">AR<span>I</span>A</div>
    <div class="aria-nav-right">
        <div class="online-pill">
            <span class="online-dot"></span>Online
        </div>
        <div class="user-chip">
            <div class="user-avatar">AA</div>
            Aleem Amjad
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="aria-hero">
    <div class="hero-greet">Welcome back</div>
    <h1>Aleem <span>Amjad</span></h1>
    <p>Your personal AI is ready — ask anything, manage your day, stay on top of everything.</p>
</div>
""", unsafe_allow_html=True)


# ── CAPABILITIES ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">✦ &nbsp; What ARIA can do</div>', unsafe_allow_html=True)
st.markdown("""
<div class="caps-grid">
    <div class="cap-card">
        <div class="cap-icon ic-1">💬</div>
        <div class="cap-info"><h4>Q &amp; A</h4><p>Answers on any topic instantly.</p></div>
    </div>
    <div class="cap-card">
        <div class="cap-icon ic-2">📅</div>
        <div class="cap-info"><h4>Calendar</h4><p>Schedules &amp; manages events.</p></div>
    </div>
    <div class="cap-card">
        <div class="cap-icon ic-3">📧</div>
        <div class="cap-info"><h4>Email</h4><p>Reads, summarizes &amp; replies.</p></div>
    </div>
    <div class="cap-card">
        <div class="cap-icon ic-4">🔍</div>
        <div class="cap-info"><h4>Web Search</h4><p>Finds live info from the web.</p></div>
    </div>
    <div class="cap-card">
        <div class="cap-icon ic-5">💰</div>
        <div class="cap-info"><h4>Finance</h4><p>Tracks expenses &amp; budget.</p></div>
    </div>
    <div class="cap-card">
        <div class="cap-icon ic-6">🧠</div>
        <div class="cap-info"><h4>Memory</h4><p>Remembers your context.</p></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── CHAT ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-divider">
    <div class="div-line"></div>
    <div class="div-label">💬 &nbsp; Chat with ARIA</div>
    <div class="div-line"></div>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask ARIA anything…")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call ARIA
    with st.chat_message("assistant"):
        with st.spinner("ARIA is thinking…"):
            reply = call_aria(user_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})