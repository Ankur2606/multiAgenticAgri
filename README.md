# Multi-Agentic Agricultural System

A comprehensive, stateful, multi-agent agricultural assistant system built with Google ADK, featuring specialized agents for crop care, weather intelligence, market analysis, government support, and financial analytics.

## 🌾 System Overview

This system implements a sophisticated multi-agent architecture with the following specialized agents:

### **Root Agent: Agricultural Multi-Agent**
- **Type**: Stateful Multi-Agent Orchestrator
- **Responsibilities**: Intelligent query routing, state management, multi-language support, session persistence

### **Specialized Agents:**

#### 🦠 **Crop Care Agent** (Sequential)
- Disease diagnosis using multimodal AI
- Treatment recommendations
- Prevention strategies
- Localized advice

#### 🌤️ **Weather Intelligence Agent** (Parallel)
- Real-time weather data collection
- Soil condition analysis
- Risk assessment
- Alert generation

#### 🌱 **Crop Advisory Agent** (Sequential)
- Soil analysis
- Climate matching
- Crop recommendations
- Hybrid variety suggestions

#### 💰 **Market Intelligence Agent** (Parallel + Blockchain)
- Real-time mandi prices
- Community price validation
- Anomaly detection
- Selling recommendations

#### 🏛️ **Government Support Agent** (Conversational)
- Scheme discovery
- Eligibility checking
- Application guidance
- Status tracking

#### 💼 **Financial Analytics Agent** (Loop)
- Income/expense tracking
- Profit margin analysis
- Revenue forecasting
- Financial reporting

#### 🛒 **Marketplace Agent** (Recommendation)
- Product recommendations
- Supplier matching
- Marketing content generation
- Quality verification

#### ❓ **FAQ Support Agent** (Knowledge Base)
- App navigation help
- Dashboard support
- General agricultural guidance
- Troubleshooting

## 🏗️ Architecture

```
🌾 AGRICULTURAL MULTI-AGENT SYSTEM
                │
                ▼
    ┌─────────────────────────────┐
    │   🤖 ROOT AGRICULTURAL     │
    │      AGENT (Stateful)      │
    │                             │
    │  • Intelligent Routing     │
    │  • State Management        │
    │  • Multi-language Support  │
    │  • Session Persistence     │
    └─────────────┬───────────────┘
                  │
    ┌─────────────┼───────────────┐
    │             │               │
    ▼             ▼               ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│🦠 CROP  │ │🌤️ WEATHER│ │🌱 CROP  │
│  CARE   │ │INTELLIGENCE│ │ADVISORY│
│(Sequential)│ │ (Parallel) │ │(Sequential)│
└─────────┘ └─────────┘ └─────────┘
    │             │               │
    ▼             ▼               ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│💰 MARKET│ │🏛️ GOVT  │ │💼 FINANCIAL│
│INTELLIGENCE│ │ SUPPORT │ │ANALYTICS│
│(Parallel + │ │(Conversational)│ │  (Loop)  │
│ Blockchain)│ │         │ │         │
└─────────┘ └─────────┘ └─────────┘
    │             │               │
    ▼             ▼               ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│🛒 MARKET│ │❓ FAQ   │ │📊 DASHBOARD│
│  PLACE  │ │ SUPPORT │ │ & ALERTS │
│(Recommendation)│ │(Knowledge Base)│ │         │
└─────────┘ └─────────┘ └─────────┘
```

## 📁 Project Structure

```
multiAgenticAgri/
├── __init__.py
├── agent.py                    # Root agricultural agent
├── .env.example                # Environment variables template
├── sub_agents/                 # Specialized agent packages
│   ├── __init__.py
│   ├── crop_care_agent/        # Sequential crop care pipeline
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── subagents/
│   │       ├── disease_diagnosis_agent/
│   │       ├── treatment_recommendation_agent/
│   │       └── prevention_strategy_agent/
│   ├── weather_intelligence_agent/  # Parallel weather analysis
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── subagents/
│   │       ├── weather_collector_agent/
│   │       ├── soil_analyzer_agent/
│   │       ├── risk_assessor_agent/
│   │       └── alert_generator_agent/
│   ├── crop_advisory_agent/    # Sequential crop recommendations
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── subagents/
│   │       ├── soil_analysis_agent/
│   │       ├── climate_matcher_agent/
│   │       └── crop_recommender_agent/
│   ├── market_intelligence_agent/  # Parallel + Blockchain
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── subagents/
│   │       ├── price_collector_agent/
│   │       ├── blockchain_validator_agent/
│   │       ├── anomaly_detector_agent/
│   │       └── recommendation_engine_agent/
│   ├── govt_support_agent/     # Conversational government support
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── financial_analytics_agent/  # Loop financial analysis
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── subagents/
│   │       ├── income_tracker_agent/
│   │       ├── expense_analyzer_agent/
│   │       ├── profit_calculator_agent/
│   │       └── forecast_generator_agent/
│   ├── marketplace_agent/      # Recommendation engine
│   │   ├── __init__.py
│   │   └── agent.py
│   └── faq_support_agent/      # Knowledge base support
│       ├── __init__.py
│       └── agent.py
├── tools/                      # Tool implementations
│   ├── __init__.py
│   ├── crop_tools.py           # Crop care and analysis tools
│   ├── weather_tools.py        # Weather and soil analysis tools
│   ├── market_tools.py         # Market and blockchain tools
│   ├── govt_tools.py           # Government scheme tools
│   ├── financial_tools.py      # Financial analysis tools
│   └── marketplace_tools.py    # Marketplace and recommendation tools
└── README.md                   # This documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Add your Google API key to .env
echo "GOOGLE_API_KEY=your_api_key_here" >> .env
```

### 2. Run the System

```bash
# From the project root directory
adk web
```

### 3. Access the Web UI

- Open your browser to `http://localhost:8000`
- Select `agricultural_multi_agent` from the dropdown
- Start interacting with the system!

## 💬 Example Interactions

### Crop Care
```
User: "My wheat crop has brown spots on the leaves. Can you help diagnose this?"
Agent: Routes to Crop Care Agent → Disease Diagnosis → Treatment → Prevention
```

### Weather Intelligence
```
User: "What's the weather forecast for my farm this week?"
Agent: Routes to Weather Intelligence Agent → Parallel data collection → Risk assessment → Alerts
```

### Market Intelligence
```
User: "What are the current mandi prices for wheat in Delhi?"
Agent: Routes to Market Intelligence Agent → Price collection → Blockchain validation → Recommendations
```

### Government Support
```
User: "What government schemes am I eligible for?"
Agent: Routes to Government Support Agent → Scheme discovery → Eligibility check → Application guidance
```

### Financial Analytics
```
User: "How is my farm's financial performance this year?"
Agent: Routes to Financial Analytics Agent → Loop analysis → Income tracking → Profit calculation → Forecasting
```

## 🔧 Agent Communication Patterns

### 1. **Sequential Execution**
- **Crop Care**: Diagnosis → Treatment → Prevention
- **Crop Advisory**: Soil Analysis → Climate Matching → Recommendations

### 2. **Parallel Execution**
- **Weather Intelligence**: Concurrent weather, soil, and risk analysis
- **Market Intelligence**: Parallel price collection, validation, and anomaly detection

### 3. **Loop Execution**
- **Financial Analytics**: Continuous monitoring and analysis cycles

### 4. **Stateful Delegation**
- **Root Agent**: Context-aware routing with persistent state

### 5. **Blockchain Validation**
- **Market Intelligence**: Distributed price data verification

## 🛠️ Tool Integration

The system includes comprehensive tool implementations for:

- **Crop Analysis**: Multimodal image analysis, disease database
- **Weather Services**: Real-time weather APIs, soil analysis
- **Market Intelligence**: Mandi price APIs, blockchain validation
- **Government Schemes**: Scheme databases, eligibility checking
- **Financial Analytics**: Income/expense tracking, forecasting
- **Marketplace**: Product recommendations, supplier verification

## 📊 State Management

The system maintains comprehensive state including:

- **User Profile**: Location, farm size, crops, preferences
- **Interaction History**: Query patterns, agent interactions
- **Financial Data**: Income, expenses, profit margins
- **Alert Subscriptions**: Weather, price, and scheme notifications
- **Session Persistence**: Continuous context across conversations

## 🔗 Integration Points

### External APIs
- Weather services (OpenWeatherMap, AccuWeather)
- Mandi price APIs (e-NAM, Agmarknet)
- Government scheme databases
- Soil data services
- SMS/notification services

### Database Requirements
- User profiles and session state
- Historical data and analytics
- Blockchain ledger for price validation
- Knowledge base for FAQ and schemes

## 🎯 Key Features

- **Multimodal Analysis**: Photo-based crop disease diagnosis
- **Real-time Intelligence**: Weather, market, and risk alerts
- **Blockchain Integration**: Community-driven price validation
- **Government Support**: Comprehensive scheme assistance
- **Financial Analytics**: Advanced profit and forecasting analysis
- **Marketplace Integration**: Product recommendations and supplier matching
- **Multi-language Support**: Hindi, English, and regional languages
- **Voice-guided Navigation**: Conversational government scheme assistance

## 🔮 Future Enhancements

- **IoT Integration**: Sensor data for real-time monitoring
- **Advanced ML Models**: Enhanced prediction and recommendation engines
- **Supply Chain Integration**: End-to-end agricultural supply chain
- **Insurance Integration**: Automated crop insurance processing
- **Global Expansion**: Multi-country agricultural support

## 📝 Notes

- This is a prototype implementation with tool stubs
- Production deployment requires integration with real APIs and databases
- Blockchain implementation is simulated for demonstration
- Financial and soil data vault features are referenced by FAQ agent
- All tools include TODO comments for production implementation

## 🤝 Contributing

This system demonstrates advanced multi-agent patterns in ADK:
- Sequential, Parallel, and Loop agent workflows
- Stateful multi-agent orchestration
- Tool integration and external API connectivity
- Blockchain and AI-powered validation systems

Perfect for hackathon demos, research, and production agricultural applications! 