import streamlit as st
from datetime import datetime
from orchestrator import PipelineOrchestrator
# from graphiti_module import build_graph     # TODO: plug your real Graphiti graph builder here
# from email_utils import send_email          # TODO: plug your real email sender here


st.write("App loaded") # DEBUG LINE

st.set_page_config(
    page_title="Medical Research RAG Bot",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Init orchestrator (cached) ----------
@st.cache_resource
def init_orchestrator():
    return PipelineOrchestrator()

orchestrator = init_orchestrator()

# ---------- Page layout ----------
st.title("🧬 Medical Research Paper RAG Bot")
st.markdown(
    "Ask a question about a medical topic (e.g., cancer, diabetes) and get the top 5 recent research papers from arXiv."
)

with st.sidebar:
    st.header("Session")
    user_email = st.text_input("Email (optional, for sending papers):", placeholder="you@example.com")
    st.markdown("---")
    st.write("Top papers and chat history are kept only in this session.")

# ---------- Session state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []        # list of {"role": "user"/"bot", "content": str}
if "last_papers" not in st.session_state:
    st.session_state.last_papers = []         # list of paper dicts from last search

# ---------- Chat + search area ----------
# Fixed: st.columns() requires a list of column ratios
col_chat, col_graph = st.columns([2, 1])

with col_chat:
    st.subheader("Chat with the Bot")

    # Show previous messages
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])

    # New user message
    prompt = st.chat_input("Ask for papers on a medical topic (e.g., 'recent papers on lung cancer treatments')")

    if prompt:
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Call orchestrator to get top papers
        with st.chat_message("assistant"):
            with st.spinner("Retrieving top 5 relevant papers from arXiv..."):
                try:
                    # You might already have something like this in orchestrator;
                    # adapt name/parameters to your actual method.
                    results = orchestrator.search_papers(prompt, n_results=5)

                    if not results or not results.get("results"):
                        reply = "No relevant papers were found. Please try rephrasing or choosing a different topic."
                        st.write(reply)
                        st.session_state.chat_history.append({"role": "bot", "content": reply})
                        st.session_state.last_papers = []
                    else:
                        papers = results["results"]
                        st.session_state.last_papers = papers

                        # Build a concise textual answer summarizing what was found
                        reply_lines = [
                            f"Found {len(papers)} relevant papers. Here are the titles:"
                        ]
                        for i, p in enumerate(papers, start=1):
                            title = p.get("title", "Untitled")
                            reply_lines.append(f"{i}. {title}")
                        reply_text = "\n".join(reply_lines)
                        st.write(reply_text)
                        st.session_state.chat_history.append({"role": "bot", "content": reply_text})

                        # Show expandable paper cards
                        st.markdown("---")
                        st.markdown("### Top 5 Papers")
                        for i, paper in enumerate(papers, start=1):
                            title = paper.get("title", "Untitled")
                            arxiv_id = paper.get("arxiv_id", "N/A")
                            abstract = paper.get("abstract", "No abstract available.")
                            similarity = paper.get("similarity", None)
                            url = paper.get("url") or f"https://arxiv.org/abs/{arxiv_id}"

                            with st.expander(f"{i}. {title}"):
                                st.markdown(f"**arXiv ID:** `{arxiv_id}`")
                                st.markdown(f"[View on arXiv]({url})")
                                if similarity is not None:
                                    st.metric("Similarity score", f"{similarity:.3f}")
                                st.markdown("**Abstract**")
                                st.write(abstract)

                except Exception as e:
                    error_msg = f"Something went wrong while searching: {e}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "bot", "content": error_msg})

with col_graph:
    st.subheader("Knowledge Graph")
    if st.session_state.last_papers:
        st.write("Graph of relationships between the retrieved papers and concepts.")
        # Placeholder for Graphiti visualization:
        # fig = build_graph(st.session_state.last_papers)
        # st.plotly_chart(fig, use_container_width=True)
        st.info(
            "Connect this section to your Graphiti-based visualization.\n"
            "Use the list of `last_papers` from session_state as the nodes/edges source."
        )
    else:
        st.info("Run a search to see the graph of related papers.")

# ---------- Email section ----------
st.markdown("---")
st.subheader("Email these papers")

# Fixed: st.columns() requires a list of column ratios
col_email_left, col_email_right = st.columns([1, 2])

with col_email_left:
    st.write(
        "After you search, you can email a list of the top 5 papers (titles + links) "
        "to yourself for later reading."
    )

with col_email_right:
    can_email = bool(st.session_state.last_papers) and bool(user_email)
    email_button = st.button("Send top 5 papers to my email", disabled=not can_email)

    if email_button:
        try:
            papers = st.session_state.last_papers
            # Build simple email body
            lines = [
                "Here are the top medical research papers you requested:",
                "",
            ]
            for i, p in enumerate(papers, start=1):
                title = p.get("title", "Untitled")
                arxiv_id = p.get("arxiv_id", "N/A")
                url = p.get("url") or f"https://arxiv.org/abs/{arxiv_id}"
                lines.append(f"{i}. {title}")
                lines.append(f"   {url}")
                lines.append("")
            lines.append(f"Sent via Medical Research RAG Bot on {datetime.now().isoformat()}")
            email_body = "\n".join(lines)

            # Call your real email sending function here
            # send_email(to_address=user_email, body=email_body)
            # For now, just pretend:
            st.success(f"Email sent to {user_email}. (Wire this to your SMTP/email function.)")

        except Exception as e:
            st.error(f"Failed to send email: {e}")