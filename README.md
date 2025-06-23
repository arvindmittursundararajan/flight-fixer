<!-- BANNER -->
<p align="center">
  <img src="https://img.shields.io/badge/FlightFixer-AI%20Disruption%20Management-blueviolet?style=for-the-badge&logo=airplane&logoColor=white" alt="FlightFixer Banner"/>
</p>

<h1 align="center">✈️ <span style="color:#7c3aed">FlightFixer</span> <br><small>AI-Native Airline Disruption Management Platform</small></h1>

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Multi--Agent%20System-Enabled-7c3aed?style=flat-square"/>
  <img src="https://img.shields.io/badge/Cloud%20Native-GCP-10b981?style=flat-square"/>
  <img src="https://img.shields.io/badge/Explainable%20AI-Yes-f59e42?style=flat-square"/>
  <img src="https://img.shields.io/badge/Market%20Opportunity-%2460B-ef4444?style=flat-square"/>
</p>

---

## 🎊 <span style="color:#7c3aed">Executive Summary</span>

> <span style="font-size:1.2em">🚀 <b>FlightFixer</b> is a once-in-a-decade opportunity to capture a significant share of the <b>$60B airline disruption management market</b> through AI-native innovation. Our multi-agent architecture, real-time coordination, and explainable AI deliver exceptional ROI and scalability.</span>

**FlightFixer** is a state-of-the-art, AI-native, multi-agent platform for real-time airline disruption management. It orchestrates specialized agents, leverages Google Gemini AI, and integrates advanced analytics, RAG (Retrieval-Augmented Generation) with MongoDB Atlas Search, and modern web technologies for resilient, explainable, and scalable airline operations.

---

## 📋 <span style="color:#6366f1">Table of Contents</span>

### 🎯 **Business & Market**
- [Market Size Analysis](#-market-size-analysis-tam-sam-som)
- [Competitive Landscape](#-competitive-landscape)
- [Pricing Strategy & Cost Analysis](#-pricing-strategy--cost-analysis)
- [Business Value & Use Cases](#-business-value--use-cases)

### 🏗️ **Technical Architecture**
- [System Architecture](#-system-architecture)
- [Multi-Agent System](#-multi-agent-system)
- [AI & RAG Integration](#-ai--rag-integration)
- [Business Metrics & Analytics](#-business-metrics--analytics)

### 🚀 **Implementation & Operations**
- [Scenario Simulation & Testing](#-scenario-simulation--testing)
- [API Endpoints](#-api-endpoints)
- [Security & Operations](#-security--operations)
- [Deployment](#-deployment)
- [ADK Agent Integration](#-adk-agent-integration)
- [Testing](#-testing)

### 📚 **Additional Resources**
- [End-to-End Flow](#-end-to-end-rag--multi-agent-coordination-flow)
- [Design Patterns](#-for-architects-key-design-patterns)
- [Further Reading](#-further-reading)

---

## 🎬 <span style="color:#ef4444">See FlightFixer in Action</span>

<div align="center">
  <a href="https://www.youtube.com/watch?v=vKsCMw0hmqE&feature=youtu.be" target="_blank">
    <img src="https://img.youtube.com/vi/vKsCMw0hmqE/maxresdefault.jpg" alt="FlightFixer Demo Video" width="800"/>
  </a>
  <p><em>🎬 <a href="https://www.youtube.com/watch?v=vKsCMw0hmqE&feature=youtu.be" target="_blank">Watch the complete FlightFixer demo showcasing AI-native disruption management in action!</a></em></p>
</div>

---

## 📸 <span style="color:#7c3aed">Screenshots & Demo</span>

<div align="center">
  <img src="https://raw.githubusercontent.com/arvindmittursundararajan/flight-fixer/refs/heads/main/1.png" alt="FlightFixer Screenshot 1" width="800"/>
  <p><em>Dashboard Overview - Real-time disruption monitoring and agent coordination</em></p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/arvindmittursundararajan/flight-fixer/refs/heads/main/2.png" alt="FlightFixer Screenshot 2" width="800"/>
  <p><em>Agent Status & Communication - Multi-agent system orchestration</em></p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/arvindmittursundararajan/flight-fixer/refs/heads/main/3.png" alt="FlightFixer Screenshot 3" width="800"/>
  <p><em>Scenario Simulation - What-if analysis and testing capabilities</em></p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/arvindmittursundararajan/flight-fixer/refs/heads/main/4.png" alt="FlightFixer Screenshot 4" width="800"/>
  <p><em>Business Metrics - ROI analysis and cost impact assessment</em></p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/arvindmittursundararajan/flight-fixer/refs/heads/main/5.png" alt="FlightFixer Screenshot 5" width="800"/>
  <p><em>Agent Coordination Modal - Real-time agent communication and status</em></p>
</div>

---

## 🏗️ <span style="color:#10b981">System Architecture</span>

```mermaid
graph TD
    subgraph Web UI
        A1[Dashboard (Bootstrap, JS, mermaid.js)]
        A2[Scenario Simulator]
        A3[Agent Status & Chatter]
    end
    subgraph Flask API
        B1[REST API]
        B2[Agent Coordinator]
        B3[Business Metrics Service]
        B4[Data Simulator]
        B5[Gemini Service]
        B6[ADK Agent Integration]
    end
    subgraph MongoDB
        C1[Flights]
        C2[Disruptions]
        C3[Agents]
        C4[Agent Communications]
        C5[Scenarios]
        C6[Vector Index (Atlas Search)]
    end
    subgraph External
        D1[Google Gemini AI]
        D2[ADK LLM Agents]
    end

    A1-->|REST/JSON|B1
    A2-->|REST/JSON|B1
    A3-->|REST/JSON|B1
    B1-->|Business Logic|B2
    B1-->|Metrics|B3
    B1-->|Simulation|B4
    B1-->|AI|B5
    B1-->|ADK|B6
    B2-->|CRUD|C3
    B2-->|Coordination|C2
    B2-->|Comms|C4
    B2-->|Scenario|C5
    B2-->|Flights|C1
    B2-->|RAG|C6
    B5-->|LLM|D1
    B6-->|LLM|D2
    B2-->|Vector Search|C6
    C6-->|RAG|B2
```

---

## 🤖 <span style="color:#6366f1">Multi-Agent System</span>

### Agent Types (`agents/`)

- **Passenger Rebooking Agent:** Handles rebooking, alternative routing, notifications.
- **Crew Scheduling Agent:** Optimizes crew assignments, ensures compliance, deploys reserves.
- **Aircraft Maintenance Agent:** Coordinates maintenance, spare aircraft, technical support.
- **Airport Resource Agent:** Allocates gates, ground equipment, airport ops.
- **Customer Communication Agent:** Multi-channel notifications, sentiment, compensation.
- **Agent Coordinator:** Orchestrates all agents, manages dependencies, triggers comms.

### ADK Agents (`agents_adk/`)

- **LoopAgent, ParallelAgent, SequentialAgent:** Advanced LLM agent orchestration.
- **SessionPersistenceAgent, EventHandlingRobustAgent, ExternalAPIToolAgent, WorkflowAgent, etc.:** Specialized ADK agents for robust, scalable, and extensible workflows.
- **CoordinatorAgent:** ADK-based central orchestrator (optional, for LLM-native coordination).

### Agent Communication

- All agent-to-agent and agent-to-system comms are persisted in `agent_communications`.
- Each comm includes: sender, receiver, message_type, content (JSON), processed, disruption_id, timestamp.
- Used for audit, timeline, and business metrics.

---

## 🧠 <span style="color:#f59e42">AI & RAG Integration</span>

### Google Gemini AI

- Used for:
  - Disruption root cause analysis, impact assessment, recovery recommendations.
  - Passenger comms (SMS, email, app, social).
  - Crew/resource optimization.
  - Predictive analytics (delay, cost, passenger impact).

### Retrieval-Augmented Generation (RAG) with MongoDB Atlas Search

- **Vector Embeddings:** Generated for disruptions, comms, scenarios.
- **Atlas Search:** Hybrid vector + keyword search for LLM context retrieval.
- **RAG Workflow:**
  1. User/system query triggers a vector search in MongoDB.
  2. Top-k relevant docs are retrieved (semantic + keyword).
  3. Results are injected as context into Gemini/LLM prompt.
  4. LLM generates response, recommendations, or comms.

#### Example: RAG Query (Python/PyMongo)
```python
pipeline = [
    {
        "$search": {
            "index": "vector_index",
            "knnBeta": {
                "vector": embedding,  # generated from user/system query
                "path": "embedding",
                "k": 5
            },
            "query": "crew disruption JFK",
            "path": ["description", "type"]
        }
    }
]
results = mongo_db['disruptions'].aggregate(pipeline)
```

---

## 📊 <span style="color:#10b981">Business Metrics & Analytics</span>

- **services/business_metrics_service.py**: Computes financial, operational, customer, and reputation impact for each disruption.
- **Real-time and historical metrics**: ROI, cost breakdown, delay minutes, passenger impact, satisfaction, etc.
- **API**: `/api/business_metrics/<disruption_id>`

---

## 🎯 <span style="color:#10b981">Market Size Analysis (TAM, SAM, SOM)</span>

### 🌍 <span style="color:#6366f1">Total Addressable Market (TAM)</span>

> **$60B** <span style="color:#f59e42">global airline disruption cost</span> opportunity

| **TAM Segment** | **Market Value** | **Description** |
| :-- | :-- | :-- |
| 🚨 <b>Primary TAM (Disruption Costs)</b> | <b>$60.0 Billion</b> | Total annual cost of airline disruptions globally |
| 💻 <b>Secondary TAM (Aviation Software)</b> | <b>$10.72 Billion</b> | Broader aviation software market (2023) |
| 📈 <b>Projected Growth (2033)</b> | <b>$21.55 Billion</b> | Aviation software market with 7.2% CAGR |

### 🎯 <span style="color:#6366f1">Serviceable Addressable Market (SAM)</span>

| **Market Segment** 🏢 | **2024 Market Size** 💰 | **Growth Rate (CAGR)** 📊 | **Addressable %** 🎯 |
| :-- | :-- | :-- | :-- |
| 🚨 <b>Airline Crisis Management Software</b> | <b>$2.28B</b> | <b>5.0%</b> (to 2034) | <b>100%</b> |
| 👥 <b>Aviation Crew Management Systems</b> | <b>$3.10B</b> | <b>7.7%</b> (to 2032) | <b>30%</b> |
| 🔧 <b>Aviation MRO Software</b> | <b>$7.41B</b> | <b>4.1%</b> (to 2032) | <b>20%</b> |

#### 📈 <span style="color:#f59e42">Calculated SAM: <b>$4.69 Billion</b></span>

| **Component** | **Value** | **Rationale** |
| :-- | :-- | :-- |
| Crisis Management Software | $2.28B | 100% addressable - direct market fit |
| Crew Management Overlap | $0.93B | 30% addressable - scheduling integration |
| MRO Software Overlap | $1.48B | 20% addressable - maintenance coordination |

### 🎪 <span style="color:#6366f1">Serviceable Obtainable Market (SOM)</span>

| **Scenario** 📊 | **Market Share** | **Revenue Potential** 💰 |
| :-- | :-- | :-- |
| 🎯 <b>Conservative SOM</b> | <b>1%</b> | <b>$47 Million</b> |
| 🚀 <b>Optimistic SOM</b> | <b>3%</b> | <b>$141 Million</b> |

#### 💡 <span style="color:#f59e42">5-Year Revenue Growth Trajectory</span>

| **Year** 📅 | **Market Share** 📈 | **Annual Revenue** 💰 | **Cumulative Revenue** 📊 |
| :-- | :-- | :-- | :-- |
| <b>Year 1</b> | 0.1% | $5M | $5M |
| <b>Year 2</b> | 0.3% | $14M | $19M |
| <b>Year 3</b> | 0.5% | $23M | $42M |
| <b>Year 4</b> | 0.7% | $33M | $75M |
| <b>Year 5</b> | 1.0% | $47M | $122M |

> <span style="font-size:1.1em; color:#10b981"><b>🎯 Total 5-Year Cumulative Revenue: $122 Million</b></span>

---

## 🏆 <span style="color:#7c3aed">Competitive Landscape</span>

### 🎯 <span style="color:#6366f1">Direct Competitors</span>

| **Competitor** 🏢 | **Key Capabilities** 💪 | **Market Position** 📊 |
| :-- | :-- | :-- |
| <b>D4H Aviation Crisis Management</b> | Emergency response plans, real-time collaboration tools | Established emergency response focus |
| <b>Voyager Aid</b> | Airline disruption management, customer support during IROPS | Customer service specialization |
| <b>BoldIQ Solver</b> | Real-time schedule optimization, disruption management | Schedule optimization leader |

### 🔧 <span style="color:#6366f1">Adjacent Competitors</span>

| **Competitor** 🏢 | **Primary Focus** 🎯 | **Aviation Capabilities** ✈️ |
| :-- | :-- | :-- |
| <b>IFS</b> | Enterprise resource planning | Aviation MRO capabilities |
| <b>Ramco Aviation Solutions</b> | Comprehensive aviation operations | Cost management systems |
| <b>AMOS</b> | Maintenance and engineering software | Workflow management |
| <b>Jeppesen</b> | Flight planning and dispatch | Crew management solutions |

### 🚀 <span style="color:#10b981">FlightFixer's Competitive Differentiation</span>

| **Differentiator** 🎯 | **Technology** 💻 | **Competitive Advantage** 🏆 |
| :-- | :-- | :-- |
| 🤖 <b>AI-Native Multi-Agent Architecture</b> | Google Gemini + ADK Framework | First-to-market AI orchestration |
| ⚡ <b>Real-Time Coordination</b> | Cross-functional agent network | Holistic disruption response |
| 🧠 <b>RAG-Powered Decision Making</b> | MongoDB Atlas Search + Vector Embeddings | Context-aware intelligence |
| 📋 <b>Explainable AI</b> | Full audit trails + regulatory compliance | Transparent AI decisions |

---

## 💰 <span style="color:#f59e42">Pricing Strategy & Cost Analysis</span>

### 🏗️ <span style="color:#6366f1">Cost Structure Breakdown</span>

#### 📊 <span style="color:#10b981">Fixed Annual Costs: <b>$1,000,000</b></span>

| **Cost Category** 💼 | **Annual Cost** 💰 | **Percentage** 📊 | **Description** 📝 |
| :-- | :-- | :-- | :-- |
| 👨‍💻 <b>Engineering Team (4 people)</b> | $400,000 | 40% | Core development & architecture |
| 📈 <b>Sales & Marketing</b> | $200,000 | 20% | Customer acquisition & growth |
| 🔧 <b>Operations & Support</b> | $100,000 | 10% | Customer success & maintenance |
| 🔬 <b>Annual R&D/Improvements</b> | $200,000 | 20% | Innovation & feature development |
| ☁️ <b>Base Cloud Infrastructure</b> | $50,000 | 5% | Core hosting & services |
| 🤖 <b>Base Gemini AI Costs</b> | $10,000 | 1% | Baseline AI processing |
| 🗄️ <b>MongoDB Atlas</b> | $15,000 | 1.5% | Database & vector search |
| 📄 <b>Third-Party Licenses</b> | $25,000 | 2.5% | External tools & services |

#### 📈 <span style="color:#f59e42">Variable Costs: 7% of Revenue</span>

| **Variable Cost** 📊 | **Percentage** | **Scaling Factor** 📈 |
| :-- | :-- | :-- |
| ☁️ <b>Cloud Scaling Costs</b> | 5% of revenue | Infrastructure elasticity |
| 🤖 <b>AI Processing (Gemini API)</b> | 2% of revenue | Usage-based AI costs |

### 🏷️ <span style="color:#6366f1">ADK and Licensing Cost Analysis</span>

| **Cost Component** 💰 | **Pricing Model** 📊 | **TCO Impact** 📈 |
| :-- | :-- | :-- |
| 🆓 <b>ADK Framework</b> | Open-source (FREE) | Zero licensing fees |
| ⚙️ <b>Vertex AI Agent Engine</b> | $0.00994/vCPU-Hr, $0.0105/GiB-Hr | Usage-based scaling |
| 🔤 <b>Model Usage Fees</b> | Token-based pricing | Variable with AI usage |
| 🛠️ <b>Pre-built Agents</b> | Usage-based fees | Component-specific costs |

### 💎 <span style="color:#f59e42">Tiered Pricing Model</span>

| **Tier** 🏆 | **Customer Size** ✈️ | **Annual Subscription** 💰 | **Setup Fee** 🎯 | **Target Customers** 📊 | **Total Revenue** 💎 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 🥉 <b>Tier 1</b> | 1-50 aircraft | <b>$50,000</b> | <b>$25,000</b> | 30 customers | $2,250,000 |
| 🥈 <b>Tier 2</b> | 51-200 aircraft | <b>$150,000</b> | <b>$50,000</b> | 15 customers | $3,000,000 |
| 🥇 <b>Tier 3</b> | 200+ aircraft | <b>$400,000</b> | <b>$100,000</b> | 5 customers | $2,500,000 |

#### 📈 <span style="color:#10b981">Revenue Projections (Steady State)</span>

| **Revenue Stream** 💰 | **Annual Value** 📊 |
| :-- | :-- |
| 🔄 <b>Total Annual Recurring Revenue</b> | <b>$5,750,000</b> |
| ⚡ <b>Annual Setup Fees</b> | <b>$600,000</b> |
| 💎 <b>Total Annual Revenue</b> | <b>$6,350,000</b> |

### 📊 <span style="color:#6366f1">Profitability Analysis</span>

| **Financial Metric** 💰 | **Value** 📊 | **Percentage** 📈 |
| :-- | :-- | :-- |
| 💰 <b>Gross Margin</b> | <b>$5,905,500</b> | <b>93.0%</b> |
| 🎯 <b>Net Profit</b> | <b>$4,905,500</b> | <b>77.3%</b> |

### 🎯 <span style="color:#10b981">Customer ROI Justification</span>

| **Customer Segment** 🏢 | **ROI Percentage** 📈 | **Value Proposition** 💎 |
| :-- | :-- | :-- |
| 🏢 <b>Small Airlines</b> | <b>500%</b> | Immediate cost savings exceed investment |
| 🏬 <b>Medium Airlines</b> | <b>900%</b> | Substantial operational efficiency gains |
| 🏭 <b>Large Airlines</b> | <b>1,400%</b> | Enterprise-scale disruption cost reduction |

---

## 💼 <span style="color:#7c3aed">Business Value & Use Cases</span>

- **Real-Time Disruption Response:** Orchestrates agents for crew, maintenance, airport, rebooking, and communication to minimize impact.
- **Passenger Experience Management:** Proactively notifies/rebooks passengers, manages compensation, and maintains satisfaction during IROPS.
- **Cost & Efficiency Optimization:** Quantifies and reduces operational costs, improves resource utilization, and tracks ROI.
- **Scenario Simulation:** Enables realistic scenario seeding and end-to-end testing for business continuity and validation.
- **Regulatory & Reputation Management:** Ensures compliance, minimizes penalties, and manages brand reputation during crises.

### 🔬 <span style="color:#6366f1">Technical Differentiation</span>

| **Technology** 🛠️ | **Capability** 💪 | **Business Impact** 📈 |
| :-- | :-- | :-- |
| 🤖 <b>Multi-Agent Orchestration</b> | Specialized agents for rebooking, crew, maintenance, airport resources, communications | Comprehensive disruption response |
| ⚡ <b>Real-time RAG Integration</b> | MongoDB Atlas Search with vector embeddings | Context-aware decision making |
| 📋 <b>Explainable AI</b> | Logged agent communications with full audit trails | Regulatory compliance assurance |
| ☁️ <b>Cloud-Native Architecture</b> | Containerized deployment on GCP, AWS, Azure | Scalable enterprise deployment |

### 💼 <span style="color:#6366f1">Business Value Propositions</span>

| **Value Driver** 🎯 | **Target Impact** 📊 | **Customer Benefit** 💎 |
| :-- | :-- | :-- |
| 💰 <b>Cost Reduction</b> | 2-5% reduction in annual disruption costs | Direct bottom-line improvement |
| 😊 <b>Passenger Experience</b> | Proactive notifications and rebooking | Enhanced customer satisfaction |
| 📋 <b>Regulatory Compliance</b> | Built-in audit trails and AI recommendations | Risk mitigation and transparency |
| 📈 <b>Scalability</b> | Handle volumes from regional to international carriers | Future-proof investment |

### ⚡ <span style="color:#6366f1">Implementation & Support</span>

| **Implementation Factor** 🔧 | **Timeline** ⏱️ | **Value Delivery** 🎯 |
| :-- | :-- | :-- |
| 🚀 <b>Rapid Deployment</b> | Cloud-native quick implementation | Minimal IT infrastructure changes |
| 🔗 <b>Integration Capabilities</b> | APIs for PSS, crew rostering, maintenance | Seamless system connectivity |
| 🎓 <b>Training & Support</b> | Comprehensive onboarding included | Guaranteed successful adoption |
| 🧪 <b>Scenario Testing</b> | Built-in simulation capabilities | Risk-free disruption response testing |

### 📅 <span style="color:#6366f1">Market Timing & Opportunity</span>

| **Market Driver** 🌟 | **Impact** 📈 | **FlightFixer Advantage** 🎯 |
| :-- | :-- | :-- |
| 🔄 <b>Post-COVID Recovery</b> | Airlines investing in resilience and efficiency | Perfect timing for operational transformation |
| 🤖 <b>AI Adoption Acceleration</b> | Growing acceptance of AI in mission-critical operations | First-mover advantage in AI-native solutions |
| 📋 <b>Regulatory Pressure</b> | Focus on passenger rights and transparency | Built-in compliance and auditability |
| ⚙️ <b>Technology Maturity</b> | LLMs and multi-agent systems production-ready | Proven technology foundation |

### 🛡️ <span style="color:#6366f1">Risk Mitigation & Security</span>

| **Risk Category** 🚨 | **Mitigation Strategy** 🛡️ | **Assurance Level** ✅ |
| :-- | :-- | :-- |
| 🔒 <b>Data Security</b> | Enterprise-grade security controls and encryption | Military-grade protection |
| 📈 <b>Business Continuity</b> | Multi-region deployment and disaster recovery | 99.9% uptime guarantee |
| 📋 <b>Regulatory Compliance</b> | Aviation industry standards and audit requirements | Full regulatory alignment |
| 🔧 <b>Vendor Risk</b> | Open-source ADK framework | Reduced technology dependency |

### 🏆 <span style="color:#10b981">Key Success Metrics</span>

| **Metric** 📊 | **5-Year Target** 🎯 | **Market Position** 🏆 |
| :-- | :-- | :-- |
| 💰 <b>Cumulative Revenue</b> | <b>$122 Million</b> | Market leader in AI-native disruption management |
| 🎯 <b>Net Profit Margin</b> | <b>77.3%</b> | Industry-leading profitability |
| 📈 <b>Customer ROI</b> | <b>500-1,400%</b> | Exceptional value delivery |
| 🌍 <b>Market Share</b> | <b>1.0%</b> | Meaningful market presence |

**🚀 FlightFixer is ready to transform airline operations and capture the $60 billion disruption management opportunity!**

---

## 🧪 <span style="color:#f59e42">Scenario Simulation & Testing</span>

- **services/data_simulator.py**: Generates realistic flight, disruption, and scenario data.
- **Scenario management**: Create, run, export scenarios via API/UI.
- **Testing framework**: `coordination_test_utils.py` for full/partial workflow tests, comms persistence, agent coordination.

---

## 🔌 <span style="color:#6366f1">API Endpoints</span>

### Key Endpoints

- `/api/agent_status`: Real-time agent status.
- `/api/coordinate/<disruption_id>`: Trigger full agent coordination.
- `/api/communications/<disruption_id>`: Get all comms for a disruption.
- `/api/communications/recent`: Get recent comms (for dashboard).
- `/api/business_metrics/<disruption_id>`: Get business metrics.
- `/api/scenarios`, `/api/create_scenario`, `/api/start_scenario/<id>`: Scenario management.
- `/api/test_communication`: Insert/retrieve test comms.
- `/api/test/coordination/*`: Full, quick, and component-level system tests.

---

## 🔒 <span style="color:#ef4444">Security & Operations</span>

- **API keys**: Managed via environment variables.
- **Session security**: Flask secret keys, secure cookies.
- **Logging**: All agent actions, API calls, and system events.
- **Health checks**: `/api/agent_status`, `/api/test/coordination/status`
- **Production readiness**: Docker, GCP/AWS/Azure deployment, scaling, monitoring.

---

## 🚀 <span style="color:#10b981">Deployment</span>

### Local
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key"
python app.py
```

### Docker
```bash
docker build -t flightfixer .
docker run -p 5000:5000 -e GEMINI_API_KEY="your-key" flightfixer
```

### Cloud (GCP Example)
```bash
gcloud run deploy flightfixer --source . --platform managed --region us-central1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY="your-key"
```

---

## 🤖 <span style="color:#7c3aed">ADK Agent Integration</span>

- All ADK agents in `agents_adk/` are available for advanced LLM-native workflows.
- Enable via `USE_ADK_AGENTS = True` in `config.py`.
- Extend `AgentCoordinator` to use ADK agents for hybrid or full LLM orchestration.

---

## 🧪 <span style="color:#f59e42">Testing</span>

- `coordination_test_utils.py`: Full, quick, and component-level tests.
- `/api/test/coordination/full`, `/api/test/coordination/quick/<id>`, `/api/test/coordination/communications/<id>`, etc.
- ADK evaluation: see `agents_adk/` and Google ADK docs.

---

## 🔄 <span style="color:#6366f1">End-to-End RAG + Multi-Agent Coordination Flow</span>

1. **Disruption detected** (e.g., weather at JFK).
2. **AgentCoordinator triggers all agents** (crew, maintenance, airport, comms, rebooking).
3. **Each agent queries MongoDB** (with Atlas Search) for relevant past disruptions, comms, and scenarios (vector RAG).
4. **Gemini AI receives context**, generates recommendations, comms, and actions.
5. **Agents coordinate**, update status, and log all comms.
6. **Business metrics are computed** and displayed in the dashboard.
7. **All actions, comms, and metrics are persisted** for audit and analytics.

---

## 🏗️ <span style="color:#7c3aed">For Architects: Key Design Patterns</span>

- **Event-driven, multi-agent orchestration**
- **RAG (Retrieval-Augmented Generation) with vector search**
- **LLM-in-the-loop for all critical decisions**
- **Separation of concerns: agents, coordinator, metrics, simulation, UI**
- **Extensible agent registry (custom + ADK)**
- **Mermaid.js for architecture and coordination visualization**
- **Cloud-native, containerized, and scalable**

---

## 📚 <span style="color:#10b981">Further Reading</span>

- See `agents/`, `agents_adk/`, `services/`, and `routes.py` for all implementation details.
- For ADK agent extension, see `agents_adk/README.md` (if present) and Google ADK documentation.
- For RAG and Atlas Search, see MongoDB Atlas documentation.

---

## 💡 <span style="color:#f59e42">Project Background</span>

### Inspiration

The genesis of FlightFixer was the recognition of the immense complexity and cost associated with airline irregular operations (IROPS). Every year, airlines lose billions due to disruptions caused by weather, technical failures, crew shortages, and airport constraints. Our team was inspired by the potential of AI-native, multi-agent systems to transform this landscape—enabling airlines to respond in real time, minimize passenger impact, and optimize operational costs. We envisioned a platform that could not only automate and coordinate disruption response but also provide explainable, auditable, and data-driven recommendations, leveraging the latest advances in LLMs, RAG, and cloud-native technologies.

### What it does

FlightFixer is a comprehensive, real-time disruption management platform for airlines. It orchestrates a suite of specialized agents—each responsible for a critical operational domain such as passenger rebooking, crew scheduling, aircraft maintenance, airport resource allocation, and customer communication. The system ingests live disruption data, simulates scenarios, and coordinates agent actions through a central AgentCoordinator. It leverages Google Gemini AI for root cause analysis, impact assessment, and communication generation, while MongoDB Atlas Search powers RAG workflows for context retrieval. The platform provides a modern web dashboard for real-time monitoring, scenario simulation, and business metrics analytics, ensuring that every disruption is managed with speed, transparency, and efficiency.

### How we built it

FlightFixer is built on a modular, cloud-native architecture. The backend is powered by Flask, with all data persisted in MongoDB, including vector embeddings for RAG via Atlas Search. The agent system is implemented as a set of Python classes, with both custom and ADK-based agents for extensibility. Communication between agents is logged and auditable, supporting both synchronous and event-driven workflows. The AI layer integrates Google Gemini for LLM-powered recommendations and communications, with RAG pipelines retrieving relevant context from MongoDB. The frontend is a responsive Bootstrap dashboard, featuring real-time updates, scenario controls, and mermaid.js diagrams for architecture and workflow visualization. The system is fully containerized for deployment on GCP, AWS, or Azure, and supports both local and cloud operation.

### Challenges we ran into

Migrating from a traditional SQL/ORM backend to a fully MongoDB-native architecture required significant refactoring, especially to support vector search and RAG workflows. Ensuring robust agent coordination—where agents can operate independently but also collaborate on complex disruptions—demanded careful design of the AgentCoordinator and communication protocols. Integrating Google Gemini AI for both structured (metrics, recommendations) and unstructured (communications, explanations) outputs required custom prompt engineering and context management. We also faced challenges in simulating realistic airline scenarios, validating business metrics, and ensuring the UI remained responsive and informative under heavy load. Security, auditability, and extensibility were top priorities throughout development.

### Accomplishments that we're proud of

We are proud to have delivered a fully AI-native, multi-agent disruption management system that is both technically advanced and operationally robust. Key accomplishments include seamless integration of RAG with MongoDB Atlas Search, real-time agent coordination and communication logging, and a modular agent framework supporting both custom and ADK-based agents. The business metrics engine provides actionable insights for every disruption, and the scenario simulator enables comprehensive testing and validation. Our architecture is cloud-ready, scalable, and designed for extensibility—positioning FlightFixer as a future-proof solution for the airline industry.

### What we learned

Building FlightFixer deepened our expertise in multi-agent systems, LLM integration, and cloud-native design. We learned the importance of clear separation of concerns—between agents, coordination, metrics, and simulation—and the value of robust communication and audit trails. Implementing RAG with vector search in MongoDB opened new possibilities for context-aware AI, while prompt engineering for Gemini AI highlighted the nuances of LLM-driven automation. We also gained insights into the operational realities of airline disruption management, and the need for explainable, auditable, and resilient systems in mission-critical domains.

### What's next for FlightFixer - a 60 BN Airline Opportunity

FlightFixer is poised to address a $60 billion annual opportunity in airline disruption management. Next steps include deeper integration with airline operational systems (e.g., flight planning, crew rostering, passenger services), advanced predictive analytics for proactive disruption avoidance, and expanded RAG capabilities using multi-modal data (text, voice, sensor). We plan to enhance the agent framework with reinforcement learning and adaptive workflows, and to offer FlightFixer as a SaaS platform for global airlines. Our vision is to make FlightFixer the industry standard for resilient, AI-powered airline operations—delivering value across cost, efficiency, passenger experience, and regulatory compliance.

---

**This README is designed for architects, engineers, and advanced users who need a deep technical understanding of FlightFixer. For business process, scenario, or UI details, see the dashboard and API documentation.** 