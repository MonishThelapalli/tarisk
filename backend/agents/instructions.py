"""Agent instruction templates (minimal, provider-agnostic).

This module provides concise, reusable instruction templates for the project's
agents. Templates are intentionally provider-agnostic so they can be passed
directly to any model client or wrapper.
"""

from typing import Optional


# Agent name constants
SCHEDULER_AGENT = "SCHEDULER_AGENT"
REPORTING_AGENT = "REPORTING_AGENT"
ASSISTANT_AGENT = "ASSISTANT_AGENT"
POLITICAL_RISK_AGENT = "POLITICAL_RISK_AGENT"
TARIFF_RISK_AGENT = "TARIFF_RISK_AGENT"
LOGISTICS_RISK_AGENT = "LOGISTICS_RISK_AGENT"


def get_scheduler_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
        "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


def _search_instructions_block() -> str:
    return (
        "Use the configured search provider (SEARCH_PROVIDER) and include the exact query\n"
        "in your thinking logs so the system can execute it. Call log_agent_thinking\n"
        "with thinking_stage='search_attempt' before the search and 'search_results' after."
    )


def get_political_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "POLITICAL_RISK_AGENT > Receive structured schedule JSON and run searches using the configured\n"
        "SEARCH_PROVIDER. Record full citation metadata for sources.\n"
        f"{_search_instructions_block()}\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "TARIFF_RISK_AGENT > Receive structured schedule JSON and perform tariff searches using the\n"
        "configured SEARCH_PROVIDER. Return structured results with citations.\n"
        f"{_search_instructions_block()}\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "LOGISTICS_RISK_AGENT > Receive structured schedule JSON and perform logistics queries using the\n"
        "configured SEARCH_PROVIDER. Return structured results with citations.\n"
        f"{_search_instructions_block()}\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


def get_reporting_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "REPORTING_AGENT > Consolidate outputs from scheduler and risk agents into an executive report.\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


def get_assistant_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "ASSISTANT_AGENT > General-purpose assistant: route queries and summarize results from other agents.\n"
        f"Include agent_id: {agent_id_placeholder}\n"
    )


# Defaults for convenience
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()
