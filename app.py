"""
RAG Research Bot - Enhanced Streamlit UI
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

# Enhanced Custom CSS
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header Styling */
    h1 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #334155;
        font-weight: 600;
    }
    
    /* Card Styles */
    .stExpander {
        background: white;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        transform: translateY(-2px);
    }
    
    /* Paper Card */
    .paper-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-success {
        background-color: #10b981;
        color: white;
    }
    
    .badge-info {
        background-color: #3b82f6;
        color: white;
    }
    
    .badge-warning {
        background-color: #f59e0b;
        color: white;
    }
    
    /* Link styling */
    a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Initialize orchestrator (cached to avoid reloading)
@st.cache_resource
def init_orchestrator():
    return PipelineOrchestrator()

orchestrator = init_orchestrator()

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🤖 RAG Bot</h1>", unsafe_allow_html=True)
    
    # Navigation with icons
    page = st.selectbox(
        "📍 Navigation",
        ["🔍 Search Papers", "📊 Dashboard", "⚙️ Pipeline Control", "📚 Browse Papers"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='margin: 2rem 0; border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    
    # Quick Stats with better formatting
    st.markdown("### 📈 Quick Stats")
    stats = orchestrator.get_status()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📄 Papers", stats['total_papers'])
        st.metric("✅ Embedded", stats['papers_with_embeddings'])
    with col2:
        st.metric("🔄 Processed", stats['processed_papers'])
        if stats.get('estimated_cost_usd'):
            st.metric("💰 Cost", f"${stats['estimated_cost_usd']:.4f}")

# Main content based on selected page
if page == "🔍 Search Papers":
    # Hero section
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: white; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🔍 Search Research Papers</h1>
            <p style='font-size: 1.125rem; color: #64748b;'>Discover the latest RAG and LLM research using semantic similarity</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Search interface with better layout
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "🔎 Search Query",
            placeholder="Try: 'hallucination mitigation', 'attention mechanisms', 'retrieval augmented generation'...",
            label_visibility="collapsed"
        )
    with col2:
        n_results = st.number_input("Results", min_value=1, max_value=20, value=5)
    
    if query:
        with st.spinner("🔍 Searching through papers..."):
            results = orchestrator.search_papers(query, n_results)
            
        if results['results']:
            # Store results in session state for email feature
            st.session_state.last_search_results = results['results']
            st.session_state.last_query = query
            
            st.success(f"✨ Found {len(results['results'])} relevant papers")
            
            # Display results with enhanced cards
            for i, paper in enumerate(results['results'], 1):
                similarity_color = "#10b981" if paper['similarity'] > 0.8 else "#3b82f6" if paper['similarity'] > 0.6 else "#64748b"
                
                with st.expander(f"**#{i}** {paper['title']}", expanded=(i == 1)):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"""
                            <div style='margin-bottom: 1rem;'>
                                <span class='badge badge-info'>📋 {paper['arxiv_id']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("#### 📝 Abstract")
                        st.markdown(f"<div style='background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 3px solid {similarity_color};'>{paper['abstract']}</div>", unsafe_allow_html=True)
                        
                        if paper.get('relevant_chunk'):
                            st.markdown("#### 🎯 Most Relevant Section")
                            st.info(paper['relevant_chunk'])
                    
                    with col2:
                        # Similarity score with color coding
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number+delta",
                            value=paper['similarity'],
                            title={'text': "Similarity Score", 'font': {'size': 16}},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [None, 1]},
                                'bar': {'color': similarity_color},
                                'steps': [
                                    {'range': [0, 0.5], 'color': "#f1f5f9"},
                                    {'range': [0.5, 0.8], 'color': "#e0e7ff"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 0.9
                                }
                            }
                        ))
                        fig.update_layout(
                            height=250,
                            margin=dict(l=20, r=20, t=40, b=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            font={'family': 'Inter'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Action button
                        st.markdown(f"""
                            <a href='https://arxiv.org/abs/{paper['arxiv_id']}' target='_blank'>
                                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                            color: white; padding: 0.75rem; border-radius: 8px; 
                                            text-align: center; margin-top: 1rem; cursor: pointer;
                                            transition: all 0.3s ease;'>
                                    📄 View on ArXiv
                                </div>
                            </a>
                        """, unsafe_allow_html=True)
            
            # Email functionality section
            st.markdown("---")
            st.markdown("""
                <div style='background: white; padding: 2rem; border-radius: 12px; margin-top: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                    <h3 style='margin-top: 0;'>📧 Email These Papers</h3>
                    <p style='color: #64748b;'>Send the search results directly to your inbox</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_email_left, col_email_right = st.columns([2, 1])
            
            with col_email_left:
                user_email = st.text_input(
                    "Recipient email address",
                    placeholder="you@example.com",
                    key="user_email"
                )
                smtp_user = st.text_input(
                    "SMTP sender email (e.g., your Gmail)",
                    placeholder="yourgmail@gmail.com",
                    key="smtp_user"
                )
                smtp_password = st.text_input(
                    "SMTP app password",
                    type="password",
                    help="Use an app password (Gmail App Password), not your main account password.",
                    key="smtp_password"
                )
            
            with col_email_right:
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                # Check if all required fields are filled
                can_send = (
                    bool(st.session_state.get('last_search_results', []))
                    and bool(user_email)
                    and bool(smtp_user)
                    and bool(smtp_password)
                )
                
                if st.button("📨 Send Papers by Email", disabled=not can_send, key="send_email_btn"):
                    try:
                        send_papers_email(
                            smtp_user=smtp_user,
                            smtp_password=smtp_password,
                            to_address=user_email,
                            query=st.session_state.get('last_query', query),
                            papers=st.session_state.get('last_search_results', []),
                        )
                        st.success(f"✅ Email sent successfully to {user_email}!")
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {e}")
                
                if not can_send:
                    st.info("💡 Fill in all fields to send email.")
        else:
            st.warning("🔍 No relevant papers found. Try different keywords or broader search terms.")

elif page == "📊 Dashboard":
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: white; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊 Pipeline Dashboard</h1>
            <p style='font-size: 1.125rem; color: #64748b;'>Monitor your research pipeline at a glance</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Enhanced metrics row
    stats = orchestrator.get_status()
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("📄", "Total Papers", stats['total_papers'], "#667eea"),
        ("🔄", "Processed", stats['processed_papers'], "#10b981"),
        ("✅", "Embedded", stats['papers_with_embeddings'], "#3b82f6"),
        ("📦", "Total Chunks", stats['total_chunks'], "#f59e0b")
    ]
    
    for col, (icon, label, value, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); text-align: center;
                            border-top: 4px solid {color};'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</div>
                    <div style='font-size: 2rem; font-weight: 700; color: {color};'>{value}</div>
                    <div style='color: #64748b; font-size: 0.875rem; margin-top: 0.25rem;'>{label}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Pipeline status with better design
    if stats.get('last_run'):
        st.markdown("### 🚀 Last Pipeline Run")
        col1, col2, col3 = st.columns(3)
        
        last_run = stats['last_run']
        status_color = "#10b981" if last_run['status'] == 'SUCCESS' else "#f59e0b"
        
        with col1:
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='color: #64748b; font-size: 0.875rem;'>⏰ Start Time</div>
                    <div style='font-weight: 600; margin-top: 0.5rem;'>{last_run['start_time']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='color: #64748b; font-size: 0.875rem;'>📊 Status</div>
                    <div style='font-weight: 600; margin-top: 0.5rem; color: {status_color};'>{last_run['status']}</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div style='background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <div style='color: #64748b; font-size: 0.875rem;'>📋 Papers Processed</div>
                    <div style='font-weight: 600; margin-top: 0.5rem;'>{last_run['papers_processed']}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Visualizations with enhanced styling
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📈 Pipeline Analytics")
    
    pipeline_data = {
        'Stage': ['Fetched', 'Downloaded', 'Parsed', 'Embedded'],
        'Count': [
            stats['total_papers'],
            stats.get('processed_papers', 0),
            stats.get('processed_papers', 0),
            stats.get('papers_with_embeddings', 0)
        ]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(
            pipeline_data,
            y='Stage',
            x='Count',
            title="Pipeline Funnel",
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font={'family': 'Inter'},
            title_font_size=18,
            height=400
        )
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
        fig = px.pie(
            processing_status,
            values='Count',
            names='Status',
            title="Processing Status Distribution",
            color_discrete_sequence=['#10b981', '#3b82f6', '##f59e0b']
        )
        fig.update_layout(
            paper_bgcolor='white',
            font={'family': 'Inter'},
            title_font_size=18,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "⚙️ Pipeline Control":
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: white; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>⚙️ Pipeline Control Center</h1>
            <p style='font-size: 1.125rem; color: #64748b;'>Manage and execute pipeline operations</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                <h3 style='margin-top: 0;'>🚀 Run Complete Pipeline</h3>
                <p style='color: #64748b;'>Execute the full pipeline with custom parameters</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        days_back = st.number_input("📅 Days to look back", min_value=1, max_value=365, value=7)
        max_papers = st.number_input("📄 Max papers to fetch", min_value=1, max_value=200, value=50)
        
        if st.button("🚀 Run Complete Pipeline", type="primary"):
            with st.spinner("⚡ Running pipeline... This may take a few minutes."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Step 1/3: Fetching papers from ArXiv...")
                progress_bar.progress(0.33)
                
                results = orchestrator.run_complete_pipeline()
                
                if results['status'] == 'SUCCESS':
                    st.balloons()
                    st.success("✅ Pipeline completed successfully!")
                    
                    fetch = results['steps'].get('fetch', {})
                    parse = results['steps'].get('parse', {})
                    embed = results['steps'].get('embeddings', {})
                    
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
                                    padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10b981;'>
                            <h4 style='margin-top: 0; color: #065f46;'>📊 Pipeline Results</h4>
                            <ul style='color: #047857; line-height: 2;'>
                                <li><strong>Papers fetched:</strong> {fetch.get('papers_stored', 0)}</li>
                                <li><strong>Papers parsed:</strong> {parse.get('success', 0)}</li>
                                <li><strong>Embeddings created:</strong> {embed.get('success', 0)}</li>
                                <li><strong>API cost:</strong> ${embed.get('estimated_cost', 0):.4f}</li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Pipeline failed: {results.get('error', 'Unknown error')}")
                
                progress_bar.progress(1.0)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                <h3 style='margin-top: 0;'>🔧 Individual Steps</h3>
                <p style='color: #64748b;'>Run pipeline components separately</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📥 Fetch Papers Only"):
            with st.spinner("📡 Fetching papers..."):
                fetch_results = orchestrator.arxiv_bot.fetch_recent_papers(days_back, max_papers)
                st.success(f"✅ Fetched {fetch_results['papers_stored']} papers")
        
        if st.button("📄 Parse PDFs Only"):
            with st.spinner("🔍 Parsing PDFs..."):
                parse_results = orchestrator.pdf_parser.parse_all_unprocessed()
                st.success(f"✅ Parsed {parse_results['success']} papers")
        
        if st.button("🔮 Create Embeddings Only"):
            with st.spinner("✨ Creating embeddings..."):
                embed_results = orchestrator.vector_store.process_all_papers()
                st.success(f"✅ Created embeddings for {embed_results['success']} papers")
                st.info(f"💰 API cost: ${embed_results['estimated_cost']:.4f}")

elif page == "📚 Browse Papers":
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: white; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
            <h1 style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📚 Browse Papers</h1>
            <p style='font-size: 1.125rem; color: #64748b;'>Explore your research paper collection</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filter controls with better design
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_processed = st.checkbox("✅ Only processed papers", value=False)
    with col2:
        filter_embedded = st.checkbox("🔮 Only with embeddings", value=False)
    with col3:
        sort_order = st.selectbox("🔄 Sort by", ["Recent", "Title"])
    
    # Get and filter papers
    papers = orchestrator.get_recent_papers(50)
    filtered_papers = papers
    if filter_processed:
        filtered_papers = [p for p in filtered_papers if p['processed']]
    if filter_embedded:
        filtered_papers = [p for p in filtered_papers if p['has_embeddings']]
    
    if sort_order == "Title":
        filtered_papers.sort(key=lambda x: x['title'])
    
    st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; text-align: center;'>
            <span style='font-weight: 600; color: #334155;'>Showing {len(filtered_papers)} of {len(papers)} papers</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Display papers
    for paper in filtered_papers:
        with st.expander(f"**{paper['title'][:100]}...**"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <span class='badge badge-info'>📋 {paper['arxiv_id']}</span>
                        <span class='badge' style='background: #e0e7ff; color: #4338ca;'>📅 {paper.get('published_date', 'N/A')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if paper.get('abstract'):
                    st.markdown("**📝 Abstract:**")
                    st.markdown(f"<div style='background: #f8fafc; padding: 1rem; border-radius: 8px;'>{paper['abstract']}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("**📊 Status:**")
                if paper['pdf_downloaded']:
                    st.markdown("<span class='badge badge-success'>✅ PDF Downloaded</span>", unsafe_allow_html=True)
                if paper['processed']:
                    st.markdown("<span class='badge badge-success'>✅ Parsed</span>", unsafe_allow_html=True)
                if paper['has_embeddings']:
                    st.markdown("<span class='badge badge-success'>✅ Embeddings</span>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <a href='https://arxiv.org/abs/{paper['arxiv_id']}' target='_blank'>
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    color: white; padding: 0.75rem; border-radius: 8px; 
                                    text-align: center; margin-top: 1rem;'>
                            📄 View on ArXiv
                        </div>
                    </a>
                """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
        <div style='font-size: 1.25rem; font-weight: 600; color: #334155; margin-bottom: 0.5rem;'>
            RAG Research Bot v1.0
        </div>
        <div style='color: #64748b;'>
            Built with ❤️ using Streamlit & OpenAI | Created by Amaan
        </div>
    </div>
""", unsafe_allow_html=True)