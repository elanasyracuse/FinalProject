"""
RAG Research Bot - Simplified Streamlit UI
Author: Amaan
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from orchestrator import PipelineOrchestrator
from email_utils import send_papers_email

# Page configuration
st.set_page_config(
    page_title="RAG Research Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simplified Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background-color: #f8fafc;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 600;
    }
    
    /* Landing Page Hero */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem 1rem 1.5rem 1rem;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: #0369a1;
        max-width: 700px;
        line-height: 1.6;
        margin-bottom: 2rem;
    }
    
    /* Search Box Styling */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: #1e293b;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        background-color: #ffffff;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #64748b;
    }
    
    /* Card Styles */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        border-color: #3b82f6;
        transform: translateY(-2px);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e3a8a !important;
        padding: 1rem !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #3b82f6 !important;
        background-color: #f1f5f9 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
        border-right: 1px solid #1e40af;
    }
    
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    /* Number inputs */
    .stNumberInput>div>div>input {
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        color: #1e293b;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        color: #1e293b;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background-color: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }
    
    .stInfo {
        background-color: #dbeafe;
        color: #1e40af;
        border: 1px solid #93c5fd;
    }
    
    .stWarning {
        background-color: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
    }
    
    .stError {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1px solid #fca5a5;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    /* Links */
    a {
        color: #3b82f6;
        text-decoration: none;
        font-weight: 500;
    }
    
    a:hover {
        color: #2563eb;
        text-decoration: underline;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #1e293b;
    }
    
    /* Text color */
    p, label, span, div {
        color: #334155;
    }
    
    /* Strong emphasis */
    strong {
        color: #1e293b;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize orchestrator
@st.cache_resource
def init_orchestrator():
    return PipelineOrchestrator()

orchestrator = init_orchestrator()

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>🤖 RAG Bot</h2>", unsafe_allow_html=True)
    
    page = st.selectbox(
        "Navigation",
        ["🔍 Search Papers", "📊 Dashboard", "⚙️ Pipeline Control", "📚 Browse Papers"]
    )
    
    st.markdown("<hr style='margin: 2rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    st.markdown("### Quick Stats")
    stats = orchestrator.get_status()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Papers", stats['total_papers'])
        st.metric("Embedded", stats['papers_with_embeddings'])
    with col2:
        st.metric("Processed", stats['processed_papers'])
        if stats.get('estimated_cost_usd'):
            st.metric("Cost", f"${stats['estimated_cost_usd']:.4f}")

# Main content based on selected page
if page == "🔍 Search Papers":
    # Hero section - simple and clean like the reference image
    st.markdown("""
        <div class='hero-container'>
            <h1 class='hero-title'>Research Paper Library</h1>
            <p class='hero-subtitle'>Explore our collection of RAG and LLM research papers using semantic search. Find the most relevant papers for your research needs.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Centered search interface
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        query = st.text_input(
            "Search",
            placeholder="Search papers by topic, methodology, or keywords...",
            label_visibility="collapsed",
            key="search_input"
        )
        
        col_a, col_b = st.columns([3, 1])
        with col_b:
            n_results = st.number_input("Results", min_value=1, max_value=20, value=5, label_visibility="collapsed")
    
    if query:
        with st.spinner("Searching through papers..."):
            results = orchestrator.search_papers(query, n_results)
            
        if results['results']:
            st.session_state.last_search_results = results['results']
            st.session_state.last_query = query
            
            st.success(f"Found {len(results['results'])} relevant papers")
            
            # Display results
            for i, paper in enumerate(results['results'], 1):
                with st.expander(f"#{i} - {paper['title']}", expanded=(i == 1)):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"**ArXiv ID:** {paper['arxiv_id']}")
                        st.markdown(f"**Similarity:** {paper['similarity']:.2%}")

                        # Show structured summary if available
                        if paper.get('has_summary') and paper.get('summary'):
                            summary = paper['summary']

                            st.markdown("### Structured Summary")

                            # Create tabs for different sections
                            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Methodology", "Results", "Related Work"])

                            with tab1:
                                if summary.get('abstract_summary'):
                                    st.markdown("**Abstract:**")
                                    st.markdown(summary['abstract_summary'])
                                if summary.get('date'):
                                    st.markdown(f"**Date:** {summary['date']}")
                                if summary.get('authors'):
                                    st.markdown(f"**Authors:** {summary['authors']}")

                            with tab2:
                                if summary.get('methodology'):
                                    st.markdown(summary['methodology'])
                                else:
                                    st.info("No methodology information available")

                            with tab3:
                                if summary.get('results'):
                                    st.markdown(summary['results'])
                                else:
                                    st.info("No results information available")

                            with tab4:
                                if summary.get('related_work'):
                                    st.markdown(summary['related_work'])
                                else:
                                    st.info("No related work information available")

                            # Show quality score if available
                            if summary.get('structure_score'):
                                st.caption(f"Summary Quality: {summary['structure_score']:.0f}%")
                        else:
                            # Fallback to abstract if no summary
                            st.markdown("**Abstract:**")
                            st.markdown(paper['abstract'])

                        if paper.get('relevant_chunk'):
                            st.markdown("**Most Relevant Section:**")
                            st.info(paper['relevant_chunk'])

                    with col2:
                        st.markdown(f"[📄 View on ArXiv](https://arxiv.org/abs/{paper['arxiv_id']})")

                        # Show summary status
                        if paper.get('has_summary'):
                            st.success("Summary Available")
                        else:
                            st.warning("No Summary")
            
            # Email section
            st.markdown("---")
            st.markdown("### 📧 Email These Papers")
            
            col1, col2 = st.columns(2)
            
            with col1:
                user_email = st.text_input("Recipient email", placeholder="you@example.com")
                smtp_user = st.text_input("SMTP sender email", placeholder="yourgmail@gmail.com")
            
            with col2:
                smtp_password = st.text_input("SMTP app password", type="password")
                
                can_send = bool(st.session_state.get('last_search_results', [])) and bool(user_email) and bool(smtp_user) and bool(smtp_password)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Send Email", disabled=not can_send):
                    try:
                        send_papers_email(
                            smtp_user=smtp_user,
                            smtp_password=smtp_password,
                            to_address=user_email,
                            query=st.session_state.get('last_query', query),
                            papers=st.session_state.get('last_search_results', []),
                        )
                        st.success(f"Email sent successfully to {user_email}!")
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")
        else:
            st.warning("No relevant papers found. Try different keywords.")

elif page == "📊 Dashboard":
    st.markdown("<h1 style='text-align: center;'>Pipeline Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Monitor your research pipeline</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    stats = orchestrator.get_status()

    # Top row - Main metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Papers", stats['total_papers'])
    with col2:
        st.metric("Processed", stats['processed_papers'])
    with col3:
        st.metric("Embedded", stats['papers_with_embeddings'])
    with col4:
        st.metric("Total Chunks", stats['total_chunks'])

    # Second row - Summary metrics (if available)
    if stats.get('total_summaries') is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Summaries Generated", stats.get('total_summaries', 0))
        with col2:
            avg_score = stats.get('avg_structure_score', 0)
            st.metric("Avg Quality Score", f"{avg_score}%")
        with col3:
            coverage = 0
            if stats['total_papers'] > 0:
                coverage = (stats.get('papers_with_summaries', 0) / stats['total_papers']) * 100
            st.metric("Summary Coverage", f"{coverage:.1f}%")
        with col4:
            model_name = stats.get('fine_tuned_model', 'Not configured')
            if model_name and model_name != 'Not configured':
                st.metric("Model Status", "Active")
            else:
                st.metric("Model Status", "Fallback")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if stats.get('last_run'):
        st.markdown("### Last Pipeline Run")
        col1, col2, col3 = st.columns(3)
        
        last_run = stats['last_run']
        
        with col1:
            st.markdown(f"**Start Time:** {last_run['start_time']}")
        with col2:
            st.markdown(f"**Status:** {last_run['status']}")
        with col3:
            st.markdown(f"**Papers Processed:** {last_run['papers_processed']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Include summaries in pipeline if available
    stages = ['Fetched', 'Downloaded', 'Parsed', 'Embedded']
    counts = [
        stats['total_papers'],
        stats.get('processed_papers', 0),
        stats.get('processed_papers', 0),
        stats.get('papers_with_embeddings', 0)
    ]

    if stats.get('total_summaries') is not None:
        stages.append('Summarized')
        counts.append(stats.get('papers_with_summaries', 0))

    pipeline_data = {
        'Stage': stages,
        'Count': counts
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(pipeline_data, y='Stage', x='Count', title="Pipeline Funnel")
        fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', font={'color': '#1e293b'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        processing_status = {
            'Status': ['Fully Processed', 'Partially Processed', 'Not Processed'],
            'Count': [
                stats.get('papers_with_embeddings', 0),
                stats.get('processed_papers', 0) - stats.get('papers_with_embeddings', 0),
                stats['total_papers'] - stats.get('processed_papers', 0)
            ]
        }
        fig = px.pie(processing_status, values='Count', names='Status', title="Processing Status")
        fig.update_layout(paper_bgcolor='#ffffff', font={'color': '#1e293b'})
        st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Pipeline Control":
    st.markdown("<h1 style='text-align: center;'>Pipeline Control</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Manage and execute pipeline operations</p>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Run Complete Pipeline")
        days_back = st.number_input("Days to look back", min_value=1, max_value=365, value=7)
        max_papers = st.number_input("Max papers to fetch", min_value=1, max_value=200, value=50)
        
        if st.button("🚀 Run Complete Pipeline", type="primary"):
            with st.spinner("Running pipeline..."):
                results = orchestrator.run_complete_pipeline()
                
                if results['status'] == 'SUCCESS':
                    st.success("Pipeline completed successfully!")

                    fetch = results['steps'].get('fetch', {})
                    parse = results['steps'].get('parse', {})
                    embed = results['steps'].get('embeddings', {})
                    summaries = results['steps'].get('summaries', {})

                    # Build results display
                    results_text = f"""
                    **Results:**
                    - Papers fetched: {fetch.get('papers_stored', 0)}
                    - Papers parsed: {parse.get('success', 0)}
                    - Embeddings created: {embed.get('success', 0)}
                    - Embedding API cost: ${embed.get('estimated_cost', 0):.4f}
                    """

                    # Add summary results if not skipped
                    if not summaries.get('skipped', False):
                        results_text += f"""
                    - Summaries generated: {summaries.get('success', 0)}
                    - Summary API cost: ${summaries.get('estimated_cost', 0):.4f}
                    - **Total API cost: ${embed.get('estimated_cost', 0) + summaries.get('estimated_cost', 0):.4f}**
                    """
                    else:
                        results_text += "\n- Summaries: Skipped (disabled or unavailable)"

                    st.markdown(results_text)
                else:
                    st.error(f"Pipeline failed: {results.get('error', 'Unknown error')}")
    
    with col2:
        st.markdown("### Individual Steps")
        
        if st.button("📥 Fetch Papers Only"):
            with st.spinner("Fetching papers..."):
                fetch_results = orchestrator.arxiv_bot.fetch_recent_papers(days_back, max_papers)
                st.success(f"Fetched {fetch_results['papers_stored']} papers")
        
        if st.button("📄 Parse PDFs Only"):
            with st.spinner("Parsing PDFs..."):
                parse_results = orchestrator.pdf_parser.parse_all_unprocessed()
                st.success(f"Parsed {parse_results['success']} papers")
        
        if st.button("🔮 Create Embeddings Only"):
            with st.spinner("Creating embeddings..."):
                embed_results = orchestrator.vector_store.process_all_papers()
                st.success(f"Created embeddings for {embed_results['success']} papers")
                st.info(f"API cost: ${embed_results['estimated_cost']:.4f}")

        if st.button("📝 Generate Summaries Only"):
            with st.spinner("Generating summaries..."):
                if orchestrator.summarizer_enabled and orchestrator.summarizer:
                    summary_results = orchestrator.summarizer.generate_summaries_batch(limit=max_papers)
                    st.success(f"Generated summaries for {summary_results['success']} papers")
                    st.info(f"API cost: ${summary_results['estimated_cost']:.4f}")
                    if summary_results['failed']:
                        st.warning(f"Failed: {len(summary_results['failed'])} papers")
                else:
                    st.error("Summarizer not available")

elif page == "📚 Browse Papers":
    st.markdown("<h1 style='text-align: center;'>Browse Papers</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Explore your research paper collection</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_processed = st.checkbox("Only processed papers", value=False)
    with col2:
        filter_embedded = st.checkbox("Only with embeddings", value=False)
    with col3:
        filter_summarized = st.checkbox("Only with summaries", value=False)
    with col4:
        sort_order = st.selectbox("Sort by", ["Recent", "Title"])
    
    papers = orchestrator.get_recent_papers(50)
    filtered_papers = papers
    if filter_processed:
        filtered_papers = [p for p in filtered_papers if p['processed']]
    if filter_embedded:
        filtered_papers = [p for p in filtered_papers if p['has_embeddings']]
    if filter_summarized:
        filtered_papers = [p for p in filtered_papers if p.get('has_summary', False)]
    
    if sort_order == "Title":
        filtered_papers.sort(key=lambda x: x['title'])
    
    st.markdown(f"**Showing {len(filtered_papers)} of {len(papers)} papers**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for paper in filtered_papers:
        with st.expander(f"{paper['title'][:100]}..."):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**ArXiv ID:** {paper['arxiv_id']}")
                st.markdown(f"**Published:** {paper.get('published_date', 'N/A')}")

                # Check if summary exists
                has_summary = paper.get('has_summary', False)

                if has_summary:
                    # Fetch and display summary
                    summary = orchestrator.db.get_paper_summary(paper['arxiv_id'])
                    if summary:
                        st.markdown("### Structured Summary")

                        # Create tabs for summary sections
                        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Methodology", "Results", "Related Work"])

                        with tab1:
                            if summary.get('abstract_summary'):
                                st.markdown("**Abstract:**")
                                st.markdown(summary['abstract_summary'])
                            if summary.get('date'):
                                st.markdown(f"**Date:** {summary['date']}")
                            if summary.get('authors'):
                                st.markdown(f"**Authors:** {summary['authors']}")

                        with tab2:
                            if summary.get('methodology'):
                                st.markdown(summary['methodology'])
                            else:
                                st.info("No methodology information available")

                        with tab3:
                            if summary.get('results'):
                                st.markdown(summary['results'])
                            else:
                                st.info("No results information available")

                        with tab4:
                            if summary.get('related_work'):
                                st.markdown(summary['related_work'])
                            else:
                                st.info("No related work information available")

                        if summary.get('structure_score'):
                            st.caption(f"Summary Quality: {summary['structure_score']:.0f}%")
                else:
                    # Show abstract if no summary
                    if paper.get('abstract'):
                        st.markdown("**Abstract:**")
                        st.markdown(paper['abstract'])

            with col2:
                st.markdown("**Status:**")
                if paper['pdf_downloaded']:
                    st.markdown("✅ PDF Downloaded")
                if paper['processed']:
                    st.markdown("✅ Parsed")
                if paper['has_embeddings']:
                    st.markdown("✅ Embeddings")
                if has_summary:
                    st.markdown("✅ Summary")

                st.markdown(f"[📄 View on ArXiv](https://arxiv.org/abs/{paper['arxiv_id']})")

                st.markdown("<br>", unsafe_allow_html=True)

                # Add summary generation button if not yet summarized
                if not has_summary and paper['processed']:
                    if st.button(f"Generate Summary", key=f"gen_{paper['arxiv_id']}"):
                        with st.spinner("Generating summary..."):
                            if orchestrator.summarizer_enabled and orchestrator.summarizer:
                                success = orchestrator.summarizer.generate_summary(paper['arxiv_id'])
                                if success:
                                    st.success("Summary generated!")
                                    st.rerun()
                                else:
                                    st.error("Failed to generate summary")
                            else:
                                st.error("Summarizer not available")
                elif has_summary:
                    if st.button(f"Regenerate", key=f"regen_{paper['arxiv_id']}"):
                        with st.spinner("Regenerating summary..."):
                            if orchestrator.summarizer_enabled and orchestrator.summarizer:
                                success = orchestrator.summarizer.regenerate_summary(paper['arxiv_id'], force=True)
                                if success:
                                    st.success("Summary regenerated!")
                                    st.rerun()
                                else:
                                    st.error("Failed to regenerate summary")
                            else:
                                st.error("Summarizer not available")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem; border-top: 1px solid #e2e8f0;'>
        <p style='color: #64748b;'>RAG Research Bot v1.0 • Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)