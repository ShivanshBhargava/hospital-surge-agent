# Hospital Surge Agent

A multi-agent AI system for intelligent hospital capacity planning during patient surges. Using Google's ADK (Agent Development Kit) with Gemini LLM, this system coordinates specialized agents to forecast surges, plan staffing, optimize inventory, and communicate with patients.

## Overview

The Hospital Surge Agent helps large urban hospitals proactively manage unpredictable patient surges caused by festivals, pollution events, epidemics, or other external factors. The system uses AI-powered agents to:

- **Forecast** patient surges 7+ days ahead using historical data and external signals
- **Plan staffing** adjustments to meet predicted demand
- **Optimize supplies** and pharmaceutical inventory
- **Communicate** risk-aware advisories to patients via SMS, email, web, and social media

## Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────┐
│  Orchestrator Agent (Chief Operations)  │
└──────────────┬──────────────────────────┘
               │
       ┌───────┼───────┬──────────┐
       ▼       ▼       ▼          ▼
    Forecast  Staffing Supply  Advisory
    Agent     Agent    Agent    Agent
       │       │       │          │
       ▼       ▼       ▼          ▼
    Tools:   Tools:  Tools:    (No tools)
    • Admissions  • Roster  • Inventory
    • Pollution   
```

### Agents

1. **Orchestrator Agent** - Coordinates the entire workflow
   - Model: `gemini-2.0-flash`
   - Role: Receives requests, delegates to specialists, synthesizes outputs
   - Output: JSON with all four specialist outputs + leadership summary

2. **Forecast Agent** - Predicts patient surges
   - Model: `gemini-2.0-flash`
   - Tools: Hospital admissions data, pollution API
   - Output: Daily surge risk levels, expected admissions, main drivers

3. **Staffing Agent** - Plans workforce adjustments
   - Model: `gemini-2.0-flash`
   - Tools: Staff roster data
   - Output: Per-day staffing recommendations, escalation plans

4. **Supply Agent** - Recommends inventory orders
   - Model: `gemini-2.0-flash`
   - Tools: Current inventory levels
   - Output: Buffer stock recommendations, ordering timeline

5. **Advisory Agent** - Creates patient communications
   - Model: `gemini-2.0-flash`
   - Role: Generates SMS, email, and social media advisories
   - Output: Risk summaries and channel-specific messages

## Features

### Data Integration
- **Historical admissions**: CSV with past admission patterns
- **Inventory management**: Real-time stock levels for critical supplies
- **Staff roster**: Current baseline staffing counts
- **External signals**: Pollution API, festival calendars, epidemic data

### Memory System
- **MemoryBank**: Stores past surge events with outcomes and tags
- **SessionStore**: Tracks current planning session
- Agents use historical context to avoid repeating past mistakes

### Output Formats
All agents produce structured JSON outputs with:
- Assumptions and risk assessments
- Detailed per-day or per-category plans
- Action timelines and escalation procedures

## Setup

### Prerequisites
- Python 3.14+
- Google Gemini API key
- Virtual environment

### Installation

```bash
# Clone repository
git clone https://github.com/ShivanshBhargava/hospital-surge-agent.git
cd hospital-surge-agent

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Environment Variables

```env
GEMINI_API_KEY=your_api_key_here
HOSPITAL_DB_URL=optional_database_url
POLLUTION_API_KEY=openweathermap_api_key
```

## Usage

### CLI Mode (Interactive)

```bash
adk run ./hospital_surge_app/
```

Example prompts:
```
Plan for the next 7 days — expected Diwali crowds and high pollution levels in Delhi
Prepare for potential flu surge in November
Generate advisories for an expected 50% increase in emergency admissions
```

### Python API

```python
from src.agents.builder import get_hospital_orchestrator

orchestrator = get_hospital_orchestrator()
# See manual_test_stub.py for detailed invocation patterns
```

## Project Structure

```
hospital-surge-agent/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── historical_admissions.csv
│   ├── inventory.csv
│   ├── roster.csv
│   └── memory.json
├── hospital_surge_app/
│   ├── __init__.py
│   └── agent.py
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration & API keys
│   ├── llm_setup.py            # Gemini client setup
│   ├── agents/
│   │   ├── orchestrator.py     # Main coordinator
│   │   ├── forecast_agent.py
│   │   ├── staffing_agent.py
│   │   ├── supply_agent.py
│   │   ├── advisory_agent.py
│   │   ├── builder.py
│   │   └── manual_test_stub.py
│   ├── tools/
│   │   ├── hospital_data_adk_tool.py
│   │   ├── hospital_data_tools.py
│   │   ├── pollution_api_tool.py
│   │   ├── inventory_tool.py
│   │   └── roster_tool.py
│   ├── memory/
│   │   ├── memory_bank.py      # Long-term memory storage
│   │   └── session_store.py    # Current session tracking
│   └── observability/
│       ├── logger.py
│       └── metrics.py
```

## Data Files

### historical_admissions.csv
```csv
date,total_admissions,icu_admissions
2025-12-01,145,23
2025-12-02,152,28
...
```

### inventory.csv
```csv
item,units_in_stock
oxygen,500
N95_masks,1200
antibiotics,850
...
```

### roster.csv
```csv
role,baseline_count
doctor,42
nurse,88
support,52
```

### memory.json
Stores past surge events:
```json
[
  {
    "event_summary": "Diwali festival spike with 40% increase",
    "staffing_outcome": {...},
    "supply_outcome": {...},
    "success_indicators": "...",
    "tags": ["festival", "diwali"]
  }
]
```

## Example Output

When you request: *"Plan for the next 7 days — expected Diwali crowds"*

The orchestrator produces JSON with:

```json
{
  "surge_forecast": {
    "horizon_days": 7,
    "daily_forecast": [
      {
        "date": "2025-12-03",
        "surge_risk": "medium",
        "expected_admissions": 185,
        "main_drivers": ["festival", "pre-holiday healthcare"]
      },
      {
        "date": "2025-12-04",
        "surge_risk": "high",
        "expected_admissions": 230,
        "main_drivers": ["diwali_crowds", "pollution"]
      }
    ]
  },
  "staffing_plan": {
    "per_day_plan": [
      {
        "date": "2025-12-04",
        "risk_level": "high",
        "recommended_additional_doctors": 8,
        "recommended_additional_nurses": 15
      }
    ]
  },
  "supply_plan": {
    "per_category_plan": [
      {
        "category": "oxygen",
        "recommended_buffer_days": 3,
        "recommended_order_quantity": 200,
        "priority": "high"
      }
    ]
  },
  "patient_advisories": {
    "patient_advisories": [
      {
        "channel": "sms",
        "target_group": "elderly",
        "message": "High pollution expected. Use masks outdoors and seek care early if needed.",
        "priority": "high"
      }
    ]
  }
}
```

## How It Works

1. **User Request**: Hospital planner asks the orchestrator for a 7-day surge plan
2. **Orchestrator Analysis**: Extracts context (Diwali, pollution, location)
3. **Parallel Specialist Calls**: Simultaneously invokes all 4 specialist agents
4. **Data Tool Execution**: Each agent calls its required tools:
   - Forecast agent reads admissions history & pollution data
   - Staffing agent checks current roster
   - Supply agent reviews inventory
   - Advisory agent uses forecast context
5. **JSON Synthesis**: Orchestrator combines all outputs into one comprehensive plan
6. **Memory Storage**: Outcome recorded for future learning

## Technologies

- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.0 Flash
- **Python**: 3.14
- **Data**: CSV files + JSON memory
- **APIs**: OpenWeather (pollution data)

## Limitations & Future Work

### Current Limitations
- Free tier Gemini API has rate limits (2 requests/min for gemini-2.5-pro)
- No real-time database integration (uses CSV)
- Naive keyword-based memory retrieval
- No persistent session history

### Future Enhancements
- Real-time hospital database integration
- Semantic search for memory retrieval
- Outcome validation against actual admissions
- Web dashboard for plan visualization
- Integration with hospital ERP systems
- Multi-hospital coordination

## Contributing

Contributions welcome! Areas for improvement:
- Better forecasting models with ML
- Real-time data connectors
- Advanced memory retrieval with embeddings
- Performance optimizations
- Additional external signals (weather, traffic, social media)

## License

MIT

## Support

For issues or questions:
1. Check the error logs: `tail -F /var/folders/q9/.../agent.latest.log`
2. Review ADK docs: https://google.github.io/adk-docs/
3. Check Gemini API quotas: https://ai.dev/usage?tab=rate-limit

---

**Last Updated**: December 2, 2025
**Status**: Functional - Rate limits managed, core features working

## Quick Test: Plain-Text Output

You can quickly verify the plain-text report output with the included script.

1. Activate your virtual environment:

```bash
source .venv/bin/activate
```

2. Run the test runner with a prompt (example):

```bash
python scripts/run_orchestrator_text.py "Plan for the next 7 days — expected Diwali crowds and high pollution levels in Delhi"
```

Notes:
- The script instantiates the orchestrator and calls it with the provided prompt. Depending on your ADK version, the call may be synchronous or asynchronous; the script handles both.
- Running the script will make calls to the Gemini API — you may encounter rate limits if your quota is exhausted.

If you'd like an automated test harness or a CI-friendly mock (no external API calls), I can add a lightweight test that stubs the LLM client and validates text-only outputs.
