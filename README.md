# Healthcare AI Engagement Platform

> **Conversational AI meets personalized care in pre-surgical support.**  
> *Inspired by Brado’s Conversational Engagement Platform case studies ([Healthcare](https://brado.net/helping-caregivers-navigate-the-dementia-journey/) & [Mya for Higher Education](https://brado.net/cep-education/))*



## 🎯 Overview

This project simulates a healthcare-focused conversational AI platform, built to explore how patient-facing agents can support pre-surgery experiences, reduce anxiety, and improve recovery outcomes through personalized interaction and domain-aware context.

The system is designed with a focus on integrating simulated vector-based retrieval, patient-specific personalization, real-time engagement analytics, and clinical empathy.



## 🧠 Project Motivation

Brado's work on **Catherine™ (Healthcare)** and **Mya (Higher Education)** demonstrates how *AI* can transform user engagement in emotionally sensitive journeys, whether navigating medical procedures or academic onboarding.

This implementation explores that concept through a simulated orthopedic care journey:  
- How can an AI agent ease anxiety pre-surgery?
- Can we personalize recovery plans using structured profiles?
- How might such a tool be evaluated from a care outcome or business value perspective?



## 🛠️ Key Features

### Conversational AI with Personalization
- Empathetic AI responses tailored to the patient's age, health profile, procedure, and support system
- Simulated multi-turn chat with dynamic context preservation
- Pre-surgery anxiety support, recovery guidance, and procedure education

### Healthcare Knowledge Retrieval
- Custom-built knowledge base with confidence scoring and medical sourcing
- Simulated vector search pipeline with keyword + context matching
- Dynamic knowledge injection based on patient queries and comorbidities

### Analytics Dashboard
- Simulated KPI tracking: engagement volume, satisfaction, anxiety trends
- Outcome simulation (e.g., recovery acceleration, pain management efficacy)
- Admin dashboard view optimized for care teams and decision-makers


### 🏥 Use Case Simulated

A 67-year-old patient (Jane Doe) preparing for a right total knee replacement with moderate anxiety. The assistant offers:
- Peer mentorship offers
- Personalized procedure explanations
- Home recovery planning
- Anxiety coping strategies and educational materials

> *This use case was inspired by published case studies on Brado's Catherine™ and Mya platforms.*



### 📊 Sample Analytics Demonstrated

| Metric                    | Value     |
|--------------------------|-----------|
| Daily Conversations      | ~60 avg   |
| Simulated Anxiety Reduction | 47.3%     |
| Patient Satisfaction     | 4.8 / 5   |
| AI Response Confidence   | 90%+ avg  |



### 📦 Tech Stack

| Component            | Tools/Frameworks                 |
|----------------------|----------------------------------|
| Frontend             | Streamlit                        |
| Data Visualization   | Plotly                           |
| AI Simulation        | Python, context-aware prompts    |
| Vector Search Logic  | Custom keyword + confidence rank |
| Session Persistence  | Streamlit session state          |
| Analytics            | Pandas                           |





## 🧭 Project Goals

- Understand design trade-offs in building domain-specific AI agents.
- Explore how vector search and patient context influence conversational relevance.
- Visualize engagement data and explore care outcome analytics.

## 🔒 Future Extensions

While this version is a sandboxed simulation, future iterations could include:

- Real OpenAI/GPT or open-source model integration.
- LangChain or LlamaIndex for true retrieval-augmented generation (RAG).
- Secure patient data handling and auth layers.
- Integration with EHRs or SMART on FHIR protocols

## 📚 Acknowledgments

This project is independently built and was inspired by public case studies from:

- [Brado’s Catherine™ Healthcare Platform](https://brado.net/helping-caregivers-navigate-the-dementia-journey/)
- [Brado’s Mya (Higher Education AI)](https://brado.net/cep-education/)
- Research on pre-surgical anxiety, orthopedic care, and conversational UX in healthcare