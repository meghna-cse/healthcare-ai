import streamlit as st
import openai
import time
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import random


st.set_page_config(
    page_title="Healthcare AI Engagement Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stApp > header {
        background: transparent;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: none !important;
    }
    .element-container div.row-widget.stRadio > div{
        flex-direction:row;
        align-items: center;
    }
    .element-container div.row-widget.stRadio > div > label{
        margin-left:7px;
    }
    .metric-card {
        background: #252c3b;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .success-metric {
        border-left-color: #2e8b57;

    }
    .warning-metric {
        border-left-color: #ff6b35;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 3px solid #1f77b4;
    }
    .patient-profile {
        background: #EBD5DD;
        color: black;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)



# Healthcare knowledge base with confidence scores and sources to simulate vector search
HEALTHCARE_KNOWLEDGE = {
    "pain_management": {
        "content": "Advanced pain management protocols show 94% of patients achieve satisfactory pain control within 48 hours post-surgery. Our multimodal approach includes: regional nerve blocks (reducing opioid need by 60%), controlled-release medications, cryotherapy, and early mobilization. Studies indicate patients using our AI-guided pain tracking report 23% better outcomes.",
        "keywords": ["pain", "hurt", "ache", "discomfort", "medication", "opioid"],
        "confidence": 0.95,
        "source": "Mayo Clinic Orthopedic Outcomes Database 2024"
    },
    "recovery_timeline": {
        "content": "Evidence-based recovery milestones: Days 1-3: Wound healing focus, assisted mobility (walker/crutches). Week 1-2: 90° knee flexion target, discharge planning. Weeks 3-6: Physical therapy intensification, 120° flexion goal. Months 2-3: Return to driving, work (desk jobs). Months 3-6: Full activity clearance. Our AI monitoring shows patients following guided protocols recover 18% faster.",
        "keywords": ["recovery", "timeline", "healing", "when", "how long", "weeks", "months"],
        "confidence": 0.92,
        "source": "American Academy of Orthopedic Surgeons Clinical Guidelines"
    },
    "procedure_details": {
        "content": "Total knee arthroplasty involves precision removal of damaged cartilage/bone, followed by implantation of titanium-cobalt femoral and tibial components with medical-grade polyethylene spacer. Modern robotic-assisted techniques (used in 78% of our cases) improve alignment accuracy by 40% and reduce recovery time by 2-3 weeks.",
        "keywords": ["procedure", "surgery", "operation", "what happens", "how", "robotic"],
        "confidence": 0.98,
        "source": "Johns Hopkins Robotic Surgery Center"
    },
    "preparation": {
        "content": "Optimized pre-surgical preparation reduces complications by 35%: Medical clearance completion, medication adjustment (stop blood thinners 7 days prior), home environment setup (shower chair, raised toilet seat), caregiver coordination, pre-hab exercises (quadriceps strengthening), and nutritional optimization (protein >1.2g/kg daily).",
        "keywords": ["prepare", "preparation", "before", "ready", "pre-op", "prehab"],
        "confidence": 0.94,
        "source": "Enhanced Recovery After Surgery (ERAS) Protocols"
    },
    "anxiety_support": {
        "content": "Clinical data shows 89% of patients experience pre-surgical anxiety. Our integrated support reduces anxiety scores by 42%: peer mentorship connections, VR-guided meditation sessions, surgeon video consultations, and 24/7 AI companion access. Patients report feeling 'significantly more prepared and confident' in 96% of cases.",
        "keywords": ["nervous", "scared", "anxious", "worried", "fear", "stress"],
        "confidence": 0.91,
        "source": "Patient Experience Research Institute"
    }
}


# Dummy patient data for personalization
PATIENT_PROFILES = {
    "jane_doe": {
        "name": "Jane Doe",
        "age": 67,
        "procedure": "Right Total Knee Replacement",
        "surgery_date": "2025-08-15",
        "surgeon": "Dr. Sarah Chen, MD",
        "anxiety_level": "Moderate",
        "support_system": "Strong Support System",
        "comorbidities": ["Hypertension", "Type 2 Diabetes"],
        "previous_surgeries": ["Appendectomy (1998)"],
        "insurance": "Medicare + Supplement"
    }
}


def generate_analytics_data():
    """Generate engagement analytics"""
    dates = pd.date_range(start='2025-01-01', end='2025-07-24', freq='D')
    
    # Patient engagement metrics
    engagement_data = pd.DataFrame({
        'Date': dates,
        'Daily_Conversations': [random.randint(45, 85) for _ in dates],
        'Avg_Session_Duration': [random.uniform(8.5, 15.2) for _ in dates],
        'Patient_Satisfaction': [random.uniform(4.6, 4.9) for _ in dates],
        'Anxiety_Reduction': [random.uniform(35, 55) for _ in dates]
    })
    
    return engagement_data



def simulate_vector_search(query, patient_context=None):
    """Vector search simulation with confidence scoring"""
    query_lower = query.lower()
    results = []
    
    for key, data in HEALTHCARE_KNOWLEDGE.items():
        matches = sum(2 if keyword in query_lower else 0 for keyword in data["keywords"])
        if matches > 0:
            # Boost confidence based on patient context
            context_boost = 0.05 if patient_context and any(
                cond.lower() in query_lower for cond in patient_context.get("comorbidities", [])
            ) else 0
            
            results.append({
                "content": data["content"],
                "confidence": min(data["confidence"] + context_boost, 1.0),
                "source": data["source"],
                "relevance_score": matches
            })
    
    # Returns highest confidence result
    return max(results, key=lambda x: x["confidence"]) if results else {
        "content": "I understand your concern. Let me provide you with specific, evidence-based information.",
        "confidence": 0.7,
        "source": "Catherine™ General Knowledge Base",
        "relevance_score": 1
    }



def generate_personalized_response(user_message, patient_profile, conversation_history):
    """Generate personalized, contextual AI response"""
    
    # Get relevant knowledge with patient context
    knowledge = simulate_advanced_vector_search(user_message, patient_profile)
    
    user_msg_lower = user_message.lower()
    patient_name = patient_profile["name"].split()[0]
    

    # Highly contextual responses with personalization
    if any(word in user_msg_lower for word in ["nervous", "scared", "worried", "anxious", "fear"]):
        response = f"Hi {patient_name}, I completely understand those feelings - especially with your surgery coming up on {patient_profile['surgery_date']}. {knowledge['content']} Given that you have {patient_profile['support_system'].lower()}, I can also connect you with other patients who've had similar experiences with Dr. {patient_profile['surgeon'].split()[-2]}. Would you like me to arrange a peer mentorship call?"
    
    elif any(word in user_msg_lower for word in ["pain", "hurt", "ache"]):
        response = f"{knowledge['content']} {patient_name}, I notice you have {', '.join(patient_profile['comorbidities'])} - Dr. {patient_profile['surgeon'].split()[-2]} will customize your pain management plan considering these conditions. Your care team has successfully managed similar cases with 97% satisfaction rates."
    
    elif any(word in user_msg_lower for word in ["recovery", "timeline", "when", "how long"]):
        response = f"{knowledge['content']} {patient_name}, considering your age ({patient_profile['age']}) and health profile, I'd expect you to follow the standard timeline closely. Since your {patient_profile['support_system'].lower()}, we can optimize your home recovery plan. Would you like me to schedule a virtual home assessment?"
    
    elif any(word in user_msg_lower for word in ["procedure", "surgery", "operation"]):
        response = f"{knowledge['content']} {patient_name}, Dr. {patient_profile['surgeon'].split()[-2]} specializes in robotic-assisted procedures and has performed over 800 successful knee replacements. Given your previous {patient_profile['previous_surgeries'][0]}, she'll review your anesthesia preferences. Would you like me to schedule a pre-op consultation video call?"
    
    else:
        response = f"{knowledge['content']} {patient_name}, I'm here to support you through every step of this journey. Is there something specific about your {patient_profile['procedure'].lower()} that you'd like me to explain further?"
    
    return {
        "response": response,
        "confidence": knowledge["confidence"],
        "source": knowledge["source"],
        "personalized": True
    }


# Initialize session state with data
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello Jane! I'm your personal AI health companion. I've been reviewing your upcoming right total knee replacement with Dr. Chen on August 15th. I know this is a big step, but you're in excellent hands - Dr. Chen has a 98.7% patient satisfaction rate. How are you feeling about everything today?",
            "timestamp": datetime.now(),
            "confidence": 0.95,
            "personalized": True
        }
    ]

if "patient_profile" not in st.session_state:
    st.session_state.patient_profile = PATIENT_PROFILES["jane_doe"]

if "analytics_data" not in st.session_state:
    st.session_state.analytics_data = generate_analytics_data()


# Sidebar with enterprise metrics
with st.sidebar:

    st.markdown("""
    <div class="patient-profile">
    <h3>👤 Jane Doe, 67</h3>
    <em>Surgery:</em> Aug 15, 2025<br>
    <em>Doctor:</em> Dr. Sarah Chen, MD<br>
    <em>Procedure:</em> Right Total Knee Replacement<br>
    <em>Anxiety Level:</em> Moderate<br>
    <em>Support:</em> Strong
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    
    if st.button("🔄 Reset Demo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    
    st.markdown("""
    ## 🏥 Demo Information
    ### Healthcare AI Assistant
    **Inspired by Catherine™ Platform**
    
    This demo simulates a conversational AI supporting patient preparing for knee replacement surgery.
    """)
    
    st.markdown("""
    ### Learn More:
    - [GitHub Repo](https://github.com/meghna-cse/healthcare-ai)
    - [About the Project](https://github.com/meghna-cse/healthcare-ai/blob/main/README.md)
    - [Architecture](https://github.com/meghna-cse/healthcare-ai/blob/main/ARCHITECTURE.md)
    """)


# Main interface with tabs
st.title("🏥 Healthcare Engagement Platform AI")
st.markdown("*Pre-Surgery Support Demo - Inspired by Brado's Catherine™ Platform*")

tab1, tab2 = st.tabs(["💬 Patient Conversation", "📈 Admin Dashboard"])

with tab1:
    # Chat interface
    st.markdown("### Pre-Surgery Support Session")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
                    if message.get("confidence"):
                        st.markdown(f"*Confidence: {message['confidence']:.1%} | Personalized: {'✔️' if message.get('personalized') else '✖️'}*")
    
    # Quick actions
    st.markdown("**Quick Actions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("😰 Pain Management Concerns", use_container_width=True):
            user_input = "I'm really worried about post-surgery pain management"
            st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            
            with st.spinner("Analyzing your concerns..."):
                time.sleep(2)
                ai_response = generate_personalized_response(user_input, st.session_state.patient_profile, st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response["response"],
                    "timestamp": datetime.now(),
                    "confidence": ai_response["confidence"],
                    "personalized": ai_response["personalized"]
                })
            st.rerun()

    with col2:
        if st.button("⏰ Recovery Timeline", use_container_width=True):
            user_input = "What should I realistically expect for my recovery timeline?"
            st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            
            with st.spinner("Personalizing timeline..."):
                time.sleep(2)
                ai_response = generate_personalized_response(user_input, st.session_state.patient_profile, st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response["response"],
                    "timestamp": datetime.now(),
                    "confidence": ai_response["confidence"],
                    "personalized": ai_response["personalized"]
                })
            st.rerun()

    with col3:
        if st.button("🤖 Robotic Surgery Info", use_container_width=True):
            user_input = "Tell me about the robotic-assisted procedure I'm having"
            st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            
            with st.spinner("Accessing procedure database..."):
                time.sleep(2)
                ai_response = generate_personalized_response(user_input, st.session_state.patient_profile, st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response["response"],
                    "timestamp": datetime.now(),
                    "confidence": ai_response["confidence"],
                    "personalized": ai_response["personalized"]
                })
            st.rerun()

    with col4:
        if st.button("👥 Connect with Peer", use_container_width=True):
            user_input = "Can you connect me with someone who's had this surgery?"
            st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
            
            with st.spinner("Finding peer matches..."):
                time.sleep(2)
                ai_response = generate_personalized_response(user_input, st.session_state.patient_profile, st.session_state.messages)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response["response"],
                    "timestamp": datetime.now(),
                    "confidence": ai_response["confidence"],
                    "personalized": ai_response["personalized"]
                })
            st.rerun()


    # Chat input
    if prompt := st.chat_input("Ask me anything about your surgery, recovery, or concerns..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": datetime.now()})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Processing with medical AI..."):
                time.sleep(2)
                
            ai_response = generate_personalized_response(prompt, st.session_state.patient_profile, st.session_state.messages)
            st.markdown(ai_response["response"])
            st.markdown(f"*Confidence: {ai_response['confidence']:.1%} | Source: {ai_response['source']}*")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": ai_response["response"],
            "timestamp": datetime.now(),
            "confidence": ai_response["confidence"],
            "personalized": ai_response["personalized"]
        })

with tab2:
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card success-metric">
        <h4>👥 Active Patients</h4>
        <h2>2,847</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card success-metric">
        <h4>💬 Conversations</h4>
        <h2>18,392</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card warning-metric">
        <h4>😌 Anxiety Reduction</h4>
        <h2>47.3%</h2>
        <small>Avg. across platform</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card success-metric">
        <h4>⚡ Response Time</h4>
        <h2>0.8s</h2>
        <small>99.9% uptime</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Engagement over time
        fig_engagement = px.line(st.session_state.analytics_data, 
                               x='Date', y='Daily_Conversations',
                               title="Daily Patient Conversations",
                               color_discrete_sequence=['#1f77b4'])
        fig_engagement.update_layout(height=400)
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col2:
        # Satisfaction trend
        fig_satisfaction = px.line(st.session_state.analytics_data, 
                                 x='Date', y='Patient_Satisfaction',
                                 title="Patient Satisfaction Score",
                                 color_discrete_sequence=['#2e8b57'])
        fig_satisfaction.update_layout(height=400)
        st.plotly_chart(fig_satisfaction, use_container_width=True)
    

    # Outcome metrics
    outcomes_data = pd.DataFrame({
        'Outcome': ['Reduced Readmissions', 'Faster Recovery', 'Higher Satisfaction', 'Lower Anxiety', 'Better Compliance'],
        'Improvement': [23, 18, 31, 47, 29],
        'Baseline': [100, 100, 100, 100, 100]
    })
    
    fig_outcomes = px.bar(outcomes_data, x='Outcome', y='Improvement',
                         title="Platform Impact vs. Traditional Care (%)",
                         color='Improvement',
                         color_continuous_scale='Viridis')
    fig_outcomes.update_layout(height=400)
    st.plotly_chart(fig_outcomes, use_container_width=True)




# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
<strong>Technical Implementation</strong>: Streamlit + Simulated Vector Search + Healthcare Knowledge Base<br><br><br>
</div>
""", unsafe_allow_html=True)