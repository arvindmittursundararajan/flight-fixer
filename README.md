# FlightFixer: AI-Powered Airline Disruption Management System

## Inspiration

The genesis of FlightFixer was the recognition of the immense complexity and cost associated with airline irregular operations (IROPS). Every year, airlines lose billions due to disruptions caused by weather, technical failures, crew shortages, and airport constraints. Our team was inspired by the potential of AI-native, multi-agent systems to transform this landscape—enabling airlines to respond in real time, minimize passenger impact, and optimize operational costs. We envisioned a platform that could not only automate and coordinate disruption response but also provide explainable, auditable, and data-driven recommendations, leveraging the latest advances in LLMs, RAG, and cloud-native technologies.

## What it does

FlightFixer is a comprehensive, real-time disruption management platform for airlines. It orchestrates a suite of specialized agents—each responsible for a critical operational domain such as passenger rebooking, crew scheduling, aircraft maintenance, airport resource allocation, and customer communication. The system ingests live disruption data, simulates scenarios, and coordinates agent actions through a central AgentCoordinator. It leverages Google Gemini AI for root cause analysis, impact assessment, and communication generation, while MongoDB Atlas Search powers RAG workflows for context retrieval. The platform provides a modern web dashboard for real-time monitoring, scenario simulation, and business metrics analytics, ensuring that every disruption is managed with speed, transparency, and efficiency.

## How we built it

FlightFixer is built on a modular, cloud-native architecture. The backend is powered by Flask, with all data persisted in MongoDB, including vector embeddings for RAG via Atlas Search. The agent system is implemented as a set of Python classes, with both custom and ADK-based agents for extensibility. Communication between agents is logged and auditable, supporting both synchronous and event-driven workflows. The AI layer integrates Google Gemini for LLM-powered recommendations and communications, with RAG pipelines retrieving relevant context from MongoDB. The frontend is a responsive Bootstrap dashboard, featuring real-time updates, scenario controls, and mermaid.js diagrams for architecture and workflow visualization. The system is fully containerized for deployment on GCP, AWS, or Azure, and supports both local and cloud operation.

## Challenges we ran into

Migrating from a traditional SQL/ORM backend to a fully MongoDB-native architecture required significant refactoring, especially to support vector search and RAG workflows. Ensuring robust agent coordination—where agents can operate independently but also collaborate on complex disruptions—demanded careful design of the AgentCoordinator and communication protocols. Integrating Google Gemini AI for both structured (metrics, recommendations) and unstructured (communications, explanations) outputs required custom prompt engineering and context management. We also faced challenges in simulating realistic airline scenarios, validating business metrics, and ensuring the UI remained responsive and informative under heavy load. Security, auditability, and extensibility were top priorities throughout development.

## Accomplishments that we're proud of

We are proud to have delivered a fully AI-native, multi-agent disruption management system that is both technically advanced and operationally robust. Key accomplishments include seamless integration of RAG with MongoDB Atlas Search, real-time agent coordination and communication logging, and a modular agent framework supporting both custom and ADK-based agents. The business metrics engine provides actionable insights for every disruption, and the scenario simulator enables comprehensive testing and validation. Our architecture is cloud-ready, scalable, and designed for extensibility—positioning FlightFixer as a future-proof solution for the airline industry.

## What we learned

Building FlightFixer deepened our expertise in multi-agent systems, LLM integration, and cloud-native design. We learned the importance of clear separation of concerns—between agents, coordination, metrics, and simulation—and the value of robust communication and audit trails. Implementing RAG with vector search in MongoDB opened new possibilities for context-aware AI, while prompt engineering for Gemini AI highlighted the nuances of LLM-driven automation. We also gained insights into the operational realities of airline disruption management, and the need for explainable, auditable, and resilient systems in mission-critical domains.

## What's next for FlightFixer - a 60 BN Airline Opportunity

FlightFixer is poised to address a $60 billion annual opportunity in airline disruption management. Next steps include deeper integration with airline operational systems (e.g., flight planning, crew rostering, passenger services), advanced predictive analytics for proactive disruption avoidance, and expanded RAG capabilities using multi-modal data (text, voice, sensor). We plan to enhance the agent framework with reinforcement learning and adaptive workflows, and to offer FlightFixer as a SaaS platform for global airlines. Our vision is to make FlightFixer the industry standard for resilient, AI-powered airline operations—delivering value across cost, efficiency, passenger experience, and regulatory compliance.

---

## Executive Summary

**FlightFixer** is a state-of-the-art, AI-native, multi-agent platform for real-time airline disruption management. It orchestrates specialized agents, leverages Google Gemini AI, and integrates advanced analytics, RAG (Retrieval-Augmented Generation) with MongoDB Atlas Search, and modern web technologies for resilient, explainable, and scalable airline operations.

---

## Table of Contents

- [Business Value & Use Cases](#business-value--use-cases)
- [System Architecture](#system-architecture)
- [Multi-Agent System](#multi-agent-system)
- [AI & RAG Integration](#ai--rag-integration)
- [Business Metrics & Analytics](#business-metrics--analytics)
- [Scenario Simulation & Testing](#scenario-simulation--testing)
- [API Endpoints](#api-endpoints)
- [Security & Operations](#security--operations)
- [Deployment](#deployment)
- [ADK Agent Integration](#adk-agent-integration)
- [Testing](#testing)
- [End-to-End Flow](#end-to-end-flow)
- [Design Patterns](#design-patterns)
- [Further Reading](#further-reading)

---

## Business Value & Use Cases

- **Real-Time Disruption Response:** Orchestrates agents for crew, maintenance, airport, rebooking, and communication to minimize impact.
- **Passenger Experience Management:** Proactively notifies/rebooks passengers, manages compensation, and maintains satisfaction during IROPS.
- **Cost & Efficiency Optimization:** Quantifies and reduces operational costs, improves resource utilization, and tracks ROI.
- **Scenario Simulation:** Enables realistic scenario seeding and end-to-end testing for business continuity and validation.
- **Regulatory & Reputation Management:** Ensures compliance, minimizes penalties, and manages brand reputation during crises.

---

## System Architecture

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

## Multi-Agent System

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

## AI & RAG Integration

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

## Business Metrics & Analytics

- **services/business_metrics_service.py**: Computes financial, operational, customer, and reputation impact for each disruption.
- **Real-time and historical metrics**: ROI, cost breakdown, delay minutes, passenger impact, satisfaction, etc.
- **API**: `/api/business_metrics/<disruption_id>`

---

## Scenario Simulation & Testing

- **services/data_simulator.py**: Generates realistic flight, disruption, and scenario data.
- **Scenario management**: Create, run, export scenarios via API/UI.
- **Testing framework**: `coordination_test_utils.py` for full/partial workflow tests, comms persistence, agent coordination.

---

## API Endpoints (Key)

- `/api/agent_status`: Real-time agent status.
- `/api/coordinate/<disruption_id>`: Trigger full agent coordination.
- `/api/communications/<disruption_id>`: Get all comms for a disruption.
- `/api/communications/recent`: Get recent comms (for dashboard).
- `/api/business_metrics/<disruption_id>`: Get business metrics.
- `/api/scenarios`, `/api/create_scenario`, `/api/start_scenario/<id>`: Scenario management.
- `/api/test_communication`: Insert/retrieve test comms.
- `/api/test/coordination/*`: Full, quick, and component-level system tests.

---

## Security & Operations

- **API keys**: Managed via environment variables.
- **Session security**: Flask secret keys, secure cookies.
- **Logging**: All agent actions, API calls, and system events.
- **Health checks**: `/api/agent_status`, `/api/test/coordination/status`
- **Production readiness**: Docker, GCP/AWS/Azure deployment, scaling, monitoring.

---

## Deployment

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

## ADK Agent Integration

- All ADK agents in `agents_adk/` are available for advanced LLM-native workflows.
- Enable via `USE_ADK_AGENTS = True` in `config.py`.
- Extend `AgentCoordinator` to use ADK agents for hybrid or full LLM orchestration.

---

## Testing

- `coordination_test_utils.py`: Full, quick, and component-level tests.
- `/api/test/coordination/full`, `/api/test/coordination/quick/<id>`, `/api/test/coordination/communications/<id>`, etc.
- ADK evaluation: see `agents_adk/` and Google ADK docs.

---

## Example: End-to-End RAG + Multi-Agent Coordination Flow

1. Disruption detected (e.g., weather at JFK).
2. AgentCoordinator triggers all agents (crew, maintenance, airport, comms, rebooking).
3. Each agent queries MongoDB (with Atlas Search) for relevant past disruptions, comms, and scenarios (vector RAG).
4. Gemini AI receives context, generates recommendations, comms, and actions.
5. Agents coordinate, update status, and log all comms.
6. Business metrics are computed and displayed in the dashboard.
7. All actions, comms, and metrics are persisted for audit and analytics.

---

## For Architects: Key Design Patterns

- **Event-driven, multi-agent orchestration**
- **RAG (Retrieval-Augmented Generation) with vector search**
- **LLM-in-the-loop for all critical decisions**
- **Separation of concerns: agents, coordinator, metrics, simulation, UI**
- **Extensible agent registry (custom + ADK)**
- **Mermaid.js for architecture and coordination visualization**
- **Cloud-native, containerized, and scalable**

---

## Further Reading

- See `agents/`, `agents_adk/`, `services/`, and `routes.py` for all implementation details.
- For ADK agent extension, see `agents_adk/README.md` (if present) and Google ADK documentation.
- For RAG and Atlas Search, see MongoDB Atlas documentation.

---

**This README is designed for architects, engineers, and advanced users who need a deep technical understanding of FlightFixer. For business process, scenario, or UI details, see the dashboard and API documentation.**
