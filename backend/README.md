# ExpRisk Backend - Project Structure

The ExpRisk backend is built on a modular, maintainable architecture that enables specialized AI agents to collaborate through a well-defined system. Here's a comprehensive overview of the project structure:

```
backend/
│
├── agents/                         # Agent-related code
│   ├── __init__.py                 # Re-exports key classes and functions
│   ├── agent_definitions.py        # Agent instructions and constants
│   ├── agent_strategies.py         # Selection and termination strategies
│   ├── agent_manager.py            # Agent creation and management
│
├── plugins/                        # Semantic Kernel plugins
│   ├── __init__.py
│   ├── schedule_plugin.py          # Equipment schedule data plugin
│   ├── risk_plugin.py              # Risk calculation plugin
│   ├── logging_plugin.py           # Agent thinking and event logging
│   ├── report_file_plugin.py       # Report generation and storage
│   ├── political_risk_json_plugin.py # Political risk data processing
│   ├── citation_handler_plugin.py  # Citation tracking from web search
│
├── managers/                       # High-level managers
│   ├── __init__.py
│   ├── chatbot_manager.py          # Handles chat interactions
│   ├── workflow_manager.py         # Automates schedule analysis workflow
│   ├── scheduler.py                # Handles scheduled runs
│
├── api/                            # API layer
│   ├── __init__.py
│   ├── app.py                      # FastAPI application
│   ├── endpoints.py                # API endpoint definitions
│   ├── api_server.py               # Standalone API server
│
├── config/                         # Configuration
│   ├── __init__.py
│   ├── settings.py                 # Application settings and env vars
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── database_utils.py           # Database connection management
│   ├── thinking_log_viewer.py      # Streamlit component for viewing agent thinking
│
├── test_scripts/                   # Testing utilities
│   ├── test_storage.py             # Storage connection tests
│   ├── test_search_agent.py        # Search integration tests
│   ├── full_test_search_agent.py   # Comprehensive search testing
│   ├── test_create_doc.py          # Document generation testing
│
├── main.py                         # Main entry point
├── streamlit_app.py                # Streamlit UI
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```

## Core Components

### Specialized Agents

The system employs multiple specialized AI agents, each designed for specific tasks:

1. **Scheduler Agent** (`SCHEDULER_AGENT`)
   - Analyzes equipment schedule data
   - Calculates risk percentages and schedule variances
   - Determines initial risk levels for equipment items
   - Prepares data for specialized risk agents

2. **Political Risk Agent** (`POLITICAL_RISK_AGENT`)
   - Monitors global political events via web search
   - Assesses geopolitical risks affecting supply chains
   - Provides sourced insights with proper citations
   - Generates structured political risk assessments

3. **Reporting Agent** (`REPORTING_AGENT`)
   - Consolidates findings from all agents
   - Creates comprehensive risk reports
   - Generates formatted Word documents
   - Stores reports in local storage or Supabase

4. **Assistant Agent** (`ASSISTANT_AGENT`)
   - Manages conversational interactions
   - Provides general information and guidance
   - Routes specialized queries to appropriate agents
   - Ensures natural, helpful responses

### Plugin System

The system uses Semantic Kernel plugins to extend functionality:

1. **EquipmentSchedulePlugin**
   - Retrieves and processes equipment schedule data
   - Connects to schedule database
   - Provides schedule comparison analytics
   - Calculates variance metrics

2. **RiskCalculationPlugin**
   - Performs risk percentage calculations
   - Categorizes risks based on percentage thresholds
   - Provides standardized risk scoring
   - Ensures consistent risk evaluation

3. **LoggingPlugin**
   - Tracks agent thinking processes
   - Logs user queries and agent responses
   - Provides detailed audit trails
   - Enables transparent AI operations

4. **ReportFilePlugin**
   - Generates formatted Word documents
   - Uploads reports to storage (local or Supabase)
   - Tracks report metadata
   - Manages document versioning

5. **PoliticalRiskJsonPlugin**
   - Converts political risk analysis to structured JSON
   - Extracts risk data from agent responses
   - Standardizes political risk information
   - Enables database storage of risk insights

6. **CitationHandlerPlugin**
   - Extracts citations from web search results
   - Formats citations for proper attribution
   - Tracks information sources
   - Ensures transparency in AI recommendations

### Management Layer

High-level managers coordinate system operations:

1. **ChatbotManager**
   - Orchestrates agent interaction for chat sessions
   - Routes user queries to appropriate agents
   - Manages conversation state
   - Handles error recovery and rate limiting

2. **WorkflowManager**
   - Automates recurring risk analysis tasks
   - Manages batch processing of equipment schedules
   - Coordinates multi-agent workflows
   - Handles scheduled report generation

3. **Scheduler**
   - Manages scheduled workflow execution
   - Supports periodic risk assessments
   - Handles time-based automation
   - Coordinates with WorkflowManager

## Technology Stack

### AI & Machine Learning
- **Google Gemini AI** - Advanced language models for reasoning and generation
- **Semantic Kernel** - Agent orchestration and plugin management
- **LangChain** (optional) - Alternative agent framework support

### Search & Information Retrieval
- **Serper API** - Real-time web search for geopolitical intelligence
- **Tavily API** - Alternative search provider
- **Citation Tracking** - Automated source attribution

### Storage Solutions
- **Local File Storage** - Simple file-based storage for development
- **Supabase Storage** - Cloud storage for production deployments
- **SQLite** - Lightweight database for local development
- **PostgreSQL** - Production-grade database for hosted deployments

### API & Web Framework
- **FastAPI** - Modern, high-performance API framework
- **Pydantic** - Data validation and settings management
- **CORS Middleware** - Cross-origin resource sharing support
- **Uvicorn** - ASGI server for production

### Document Generation
- **Spire.Doc.Free** - Word document generation
- **Python-docx** - Alternative document manipulation
- **ReportLab** (optional) - PDF generation support

## Running Options

### 1. Streamlit Developer Interface
```bash
streamlit run streamlit_app.py
```
Launches the Streamlit interface with chat, visualization, and developer tools

### 2. FastAPI Server
```bash
cd api
python api_server.py
```
Starts the REST API server for frontend integration

### 3. Standalone Testing
```bash
python main.py
```
Run specific test scenarios or custom workflows

## Agent Interaction Patterns

The system supports multiple interaction patterns:

### Interactive Chat Flow
For schedule/risk related questions in chat:
```
User Query → SCHEDULER_AGENT → REPORTING_AGENT → Response
```

### Specialized Risk Analysis
For political risk analysis:
```
User Query → SCHEDULER_AGENT → POLITICAL_RISK_AGENT → REPORTING_AGENT → Response
```

### Automated Workflow
For scheduled analysis:
```
Scheduler → WorkflowManager → SCHEDULER_AGENT → POLITICAL_RISK_AGENT → REPORTING_AGENT → Report Storage
```

## Required Environment Variables

The application requires these environment variables in a `.env` file:

```properties
# =============================
# 🌐 AI / MODEL CONFIGURATION
# =============================
AI_MODEL_PROVIDER=google
AI_MODEL_NAME=gemini-2.5-pro
GOOGLE_API_KEY=your_google_api_key

# =============================
# 🧠 DATABASE CONFIGURATION
# =============================
# For local development (SQLite)
DB_CONNECTION_STRING=sqlite:///local.db

# Example if you use hosted Postgres (optional alternative)
# DB_CONNECTION_STRING=postgresql://user:password@db.example.com/your_db_name

# =============================
# 📦 STORAGE CONFIGURATION
# =============================
# Use local uploads folder
STORAGE_PATH=./uploads

# Optional: if you use Supabase Storage instead
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your_supabase_anon_key

# =============================
# 🔍 SEARCH CONFIGURATION
# =============================
# Choose your search provider (serper or tavily recommended)
SEARCH_PROVIDER=serper
SEARCH_API_KEY=your_search_api_key

# Optional: for Tavily Search
# SEARCH_PROVIDER=tavily
# SEARCH_API_KEY=your_tavily_api_key

# =============================
# ⚙️ APP CONFIGURATION
# =============================
# General FastAPI / Streamlit settings
APP_ENV=development
LOG_LEVEL=info
PORT=8000
```

## Installation & Setup

### 1. Clone and Setup Virtual Environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file with the required variables (see above)

### 4. Initialize Database
```bash
# For SQLite (automatic)
# For PostgreSQL, run migrations if needed
python -m alembic upgrade head
```

### 5. Test Configuration
```bash
# Run connection tests
python test_scripts/test_storage.py
python test_scripts/test_search_agent.py
```

### 6. Start the Application
```bash
# Option A: Developer mode
streamlit run streamlit_app.py

# Option B: API server
cd api
python api_server.py
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat` - Process user message and return agent response
- `GET /api/chat/history/{session_id}` - Retrieve chat history
- `DELETE /api/chat/session/{session_id}` - Clear chat session

### Report Endpoints
- `GET /api/reports` - List all generated reports
- `GET /api/reports/{report_id}` - Get specific report
- `GET /api/reports/{report_id}/download` - Download report file
- `DELETE /api/reports/{report_id}` - Delete report

### System Endpoints
- `GET /api/health` - System health check
- `GET /api/version` - API version info
- `GET /api/thinking-logs/{session_id}` - Get agent thinking logs

## Development Guidelines

### Adding New Agents
1. Define agent instructions in `agents/agent_definitions.py`
2. Register agent in `agents/agent_manager.py`
3. Update selection strategy in `agents/agent_strategies.py`
4. Test agent interaction patterns

### Creating New Plugins
1. Create plugin class in `plugins/` directory
2. Implement required methods with `@kernel_function` decorator
3. Register plugin in agent initialization
4. Document plugin capabilities

### Error Handling
- Use try-except blocks for external API calls
- Log errors with appropriate severity levels
- Implement retry logic for transient failures
- Return user-friendly error messages

### Testing
- Write unit tests for plugins and utilities
- Test agent interaction flows end-to-end
- Validate search integration and citation tracking
- Test storage operations (local and cloud)

## Troubleshooting

### Common Issues

1. **Search API Errors**
   - Verify API key is correct
   - Check rate limits
   - Ensure network connectivity

2. **Database Connection Issues**
   - Verify connection string format
   - Check database permissions
   - Ensure database exists

3. **Storage Errors**
   - Verify storage path exists and is writable
   - Check Supabase credentials if using cloud storage
   - Ensure adequate disk space

4. **Agent Timeout Issues**
   - Increase timeout values in configuration
   - Check model availability
   - Review agent prompt complexity

### Debug Mode
Enable detailed logging:
```python
LOG_LEVEL=debug
```

View agent thinking process in Streamlit developer view

## Performance Optimization

### Caching
- Enable result caching for frequent queries
- Cache search results to reduce API calls
- Use database query optimization

### Rate Limiting
- Configure rate limits for external APIs
- Implement exponential backoff for retries
- Monitor API usage and quotas

### Async Operations
- Use async/await for I/O operations
- Parallel processing for independent tasks
- Background tasks for report generation

## Security Considerations

- Store API keys in environment variables only
- Use HTTPS for API communications
- Validate all user inputs
- Implement proper authentication/authorization
- Regular security audits of dependencies
- Secure storage of sensitive data

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request with clear description

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review test scripts for examples
