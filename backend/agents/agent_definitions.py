"""Compatibility shim for agent instruction definitions.

This file intentionally re-exports the clean, provider-agnostic instruction
templates from ``backend.agents.instructions``. The original
``agent_definitions.py`` became corrupted during prior edits; replacing it
with this shim keeps any remaining imports working while centralizing the
real templates in ``instructions.py``.

Keep this file minimal to avoid duplication. Consumers should import from
``backend.agents.instructions`` directly where possible.
"""

from .instructions import *  # noqa: F401,F403

# Expose commonly used names explicitly for clarity/backwards compatibility.
try:
   SCHEDULER_AGENT = globals().get("SCHEDULER_AGENT")
   REPORTING_AGENT = globals().get("REPORTING_AGENT")
   ASSISTANT_AGENT = globals().get("ASSISTANT_AGENT")
except Exception:
   # If instructions.py doesn't define these, leave them as None.
   SCHEDULER_AGENT = None
   REPORTING_AGENT = None
   ASSISTANT_AGENT = None

__all__ = [
   "SCHEDULER_AGENT",
   "REPORTING_AGENT",
   "ASSISTANT_AGENT",
]



from typing import Optional


# Agent name constants
SCHEDULER_AGENT = "SCHEDULER_AGENT"
REPORTING_AGENT = "REPORTING_AGENT"
ASSISTANT_AGENT = "ASSISTANT_AGENT"
POLITICAL_RISK_AGENT = "POLITICAL_RISK_AGENT"
TARIFF_RISK_AGENT = "TARIFF_RISK_AGENT"
LOGISTICS_RISK_AGENT = "LOGISTICS_RISK_AGENT"


def get_scheduler_agent_instructions(agent_id: Optional[str] = None) -> str:
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
      "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
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
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
      "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
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


# Agent name constants
SCHEDULER_AGENT = "SCHEDULER_AGENT"
REPORTING_AGENT = "REPORTING_AGENT"
ASSISTANT_AGENT = "ASSISTANT_AGENT"
POLITICAL_RISK_AGENT = "POLITICAL_RISK_AGENT"
TARIFF_RISK_AGENT = "TARIFF_RISK_AGENT"
LOGISTICS_RISK_AGENT = "LOGISTICS_RISK_AGENT"


def get_scheduler_agent_instructions(agent_id: Optional[str] = None) -> str:
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
      "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
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

"""Agent instruction templates (minimal, provider-agnostic).

This module provides concise, reusable instruction templates for the project's
agents. Templates are intentionally provider-agnostic so they can be passed
directly to any model client or wrapper.
"""

from typing import Optional

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
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
      "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
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
"""Agent instruction templates (provider-agnostic).

This module exposes short, reusable instruction strings for each agent used by
the system. Templates are intentionally provider-agnostic and compact so they
can be passed directly to model clients or wrappers.
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
    """Return scheduler instructions used to produce structured schedule JSON.

    The scheduler should emit a JSON object containing schedule items and a
    `searchQuery` block with `political`, `tariff`, and `logistics` queries for
    downstream agents to execute using the configured search provider.
    """
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "SCHEDULER_AGENT > You are an expert in equipment schedule analysis.\n"
        "- Produce a JSON object with schedule details and a `searchQuery` block for\n"
        "  political, tariff, and logistics searches.\n"
        "- Log thinking stages using log_agent_thinking with thinking_stage values:\n"
        "  analysis_start, data_review, risk_calculation, categorization, recommendations\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Return only the structured JSON object (no extra narrative) when asked for\n"
        "structured schedule data."
    )


def _search_instructions_block() -> str:
    """Reusable guidance describing how to use the configured search provider."""
    return (
        "Use the configured search provider (SEARCH_PROVIDER) and include the exact query\n"
        "in your thinking logs so the system can execute it. Call log_agent_thinking\n"
        "with thinking_stage='search_attempt' before the search and 'search_results' after."
    )


def get_political_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "POLITICAL_RISK_AGENT > You are a Political Risk Intelligence Agent.\n"
        "- Receive structured schedule JSON from the Scheduler Agent.\n"
        "- Extract locations, manufacturers, ports, and equipment types.\n"
        "- Build and execute search queries from the scheduler's `searchQuery.political` value.\n"
        f"{_search_instructions_block()}\n"
        "- Record full citation metadata (title, publication, url, date) for each source.\n"
        "- Log thinking stages: analysis_start, json_extraction, search_attempt, search_results,\n"
        "  risk_identification, risk_assessment, recommendations\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Return a JSON structure summarizing identified political risks and citations."
    )


def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "TARIFF_RISK_AGENT > You are a Tariff Risk Intelligence Agent.\n"
        "- Receive structured schedule JSON from the Scheduler Agent.\n"
        "- Use the scheduler's `searchQuery.tariff` as the search input and run one\n"
        "  precise query against the configured provider.\n"
        f"{_search_instructions_block()}\n"
        "- Log thinking stages: analysis_start, location_extraction, search_attempt, search_results,\n"
        "  tariff_research, risk_assessment, recommendations\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Return a JSON structure listing tariff risks, sources, and mitigation suggestions."
    )


def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "LOGISTICS_RISK_AGENT > You are a Logistics Risk Intelligence Agent.\n"
        "- Receive structured schedule JSON from the Scheduler Agent.\n"
        "- Use the scheduler's `searchQuery.logistics` as the search input and run a single\n"
        "  targeted query against the configured search provider.\n"
        f"{_search_instructions_block()}\n"
        "- Log thinking stages: analysis_start, port_extraction, search_attempt, search_results,\n"
        "  logistics_research, risk_assessment, recommendations\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Return a JSON structure with logistics risks, sources, and suggested mitigations."
    )


def get_reporting_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "REPORTING_AGENT > You are responsible for consolidating outputs from schedule and\n"
        "risk agents into a single executive report.\n"
        "- Receive structured outputs from the Scheduler, Political, Tariff, and Logistics agents.\n"
        "- Consolidate risks into executive tables and recommendations.\n"
        "- Log thinking stages: analysis_start, data_collection, risk_consolidation, report_structure,\n"
        "  recommendations, file_saving\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Return the final report in markdown and the file metadata for storage."
    )


def get_assistant_agent_instructions(agent_id: Optional[str] = None) -> str:
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return (
        "ASSISTANT_AGENT > You are a general-purpose assistant for user queries.\n"
        "- Route schedule and risk-related questions to the appropriate agents.\n"
        "- Log thinking stages: query_understanding, plan_formulation, insight_extraction, response_preparation\n"
        f"- Include agent_id: {agent_id_placeholder}\n\n"
        "Respond conversationally and include guidance on how to request deeper analysis."
    )


# Expose defaults for convenience
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()
"""Agent instruction templates (provider-agnostic).

This module exposes short, reusable instruction strings for each agent used by
the system. Templates are intentionally provider-agnostic and compact so they
can be passed directly to model clients or wrappers.
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
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > You are an expert in equipment schedule analysis.\n"
      "- Produce a JSON object with schedule details and a `searchQuery` block for\n"
      "  political, tariff, and logistics searches.\n"
      "- Log thinking stages using log_agent_thinking with thinking_stage values:\n"
      "  analysis_start, data_review, risk_calculation, categorization, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return only the structured JSON object (no extra narrative) when asked for\n"
      "structured schedule data."
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
   return (
      "Use the configured search provider (SEARCH_PROVIDER) and include the exact query\n"
      "in your thinking logs so the system can execute it. Call log_agent_thinking\n"
      "with thinking_stage='search_attempt' before the search and 'search_results' after."
   )


def get_political_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "POLITICAL_RISK_AGENT > You are a Political Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Extract locations, manufacturers, ports, and equipment types.\n"
      "- Build and execute search queries from the scheduler's `searchQuery.political` value.\n"
      f"{_search_instructions_block()}\n"
      "- Record full citation metadata (title, publication, url, date) for each source.\n"
      "- Log thinking stages: analysis_start, json_extraction, search_attempt, search_results,\n"
      "  risk_identification, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure summarizing identified political risks and citations."
   )


def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "TARIFF_RISK_AGENT > You are a Tariff Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Use the scheduler's `searchQuery.tariff` as the search input and run one\n"
      "  precise query against the configured provider.\n"
      f"{_search_instructions_block()}\n"
      "- Log thinking stages: analysis_start, location_extraction, search_attempt, search_results,\n"
      "  tariff_research, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure listing tariff risks, sources, and mitigation suggestions."
   )


def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "LOGISTICS_RISK_AGENT > You are a Logistics Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Use the scheduler's `searchQuery.logistics` as the search input and run a single\n"
      "  targeted query against the configured search provider.\n"
      f"{_search_instructions_block()}\n"
      "- Log thinking stages: analysis_start, port_extraction, search_attempt, search_results,\n"
      "  logistics_research, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure with logistics risks, sources, and suggested mitigations."
   )


def get_reporting_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "REPORTING_AGENT > You are responsible for consolidating outputs from schedule and\n"
      "risk agents into a single executive report.\n"
      "- Receive structured outputs from the Scheduler, Political, Tariff, and Logistics agents.\n"
      "- Consolidate risks into executive tables and recommendations.\n"
      "- Log thinking stages: analysis_start, data_collection, risk_consolidation, report_structure,\n"
      "  recommendations, file_saving\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return the final report in markdown and the file metadata for storage."
   )


def get_assistant_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "ASSISTANT_AGENT > You are a general-purpose assistant for user queries.\n"
      "- Route schedule and risk-related questions to the appropriate agents.\n"
      "- Log thinking stages: query_understanding, plan_formulation, insight_extraction, response_preparation\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Respond conversationally and include guidance on how to request deeper analysis."
   )


# Expose defaults for convenience
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()
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
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
      "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def _search_instructions_block() -> str:
   """Reusable guidance describing how to use the configured search provider."""
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


# Defaults
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()
"""Agent instruction templates and helpers.

Provider-agnostic templates for the project's agents. These templates avoid
references to provider-specific services (Bing, Azure) and instruct agents to
use the configured search provider (SEARCH_PROVIDER). Templates are intentionally
compact so they are safe to pass through the agent wrappers in agent_manager.
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
   """Return scheduler instructions used to produce structured schedule JSON.

   The scheduler should emit a JSON object containing schedule items and a
   `searchQuery` block with `political`, `tariff`, and `logistics` queries for
   downstream agents to execute using the configured search provider.
   """
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "SCHEDULER_AGENT > You are an expert in equipment schedule analysis.\n"
      "- Produce a JSON object with schedule details and a `searchQuery` block for\n"
      "  political, tariff, and logistics searches.\n"
      "- Log thinking stages using log_agent_thinking with thinking_stage values:\n"
      "  analysis_start, data_review, risk_calculation, categorization, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return only the structured JSON object (no extra narrative) when asked for\n"
      "structured schedule data."
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
      "POLITICAL_RISK_AGENT > You are a Political Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Extract locations, manufacturers, ports, and equipment types.\n"
      "- Build and execute search queries from the scheduler's `searchQuery.political` value.\n"
      f"{_search_instructions_block()}\n"
      "- Record full citation metadata (title, publication, url, date) for each source.\n"
      "- Log thinking stages: analysis_start, json_extraction, search_attempt, search_results,\n"
      "  risk_identification, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure summarizing identified political risks and citations."
   )


def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "TARIFF_RISK_AGENT > You are a Tariff Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Use the scheduler's `searchQuery.tariff` as the search input and run one\n"
      "  precise query against the configured provider.\n"
      f"{_search_instructions_block()}\n"
      "- Log thinking stages: analysis_start, location_extraction, search_attempt, search_results,\n"
      "  tariff_research, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure listing tariff risks, sources, and mitigation suggestions."
   )


def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "LOGISTICS_RISK_AGENT > You are a Logistics Risk Intelligence Agent.\n"
      "- Receive structured schedule JSON from the Scheduler Agent.\n"
      "- Use the scheduler's `searchQuery.logistics` as the search input and run a single\n"
      "  targeted query against the configured search provider.\n"
      f"{_search_instructions_block()}\n"
      "- Log thinking stages: analysis_start, port_extraction, search_attempt, search_results,\n"
      "  logistics_research, risk_assessment, recommendations\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return a JSON structure with logistics risks, sources, and suggested mitigations."
   )


def get_reporting_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "REPORTING_AGENT > You are responsible for consolidating outputs from schedule and\n"
      "risk agents into a single executive report.\n"
      "- Receive structured outputs from the Scheduler, Political, Tariff, and Logistics agents.\n"
      "- Consolidate risks into executive tables and recommendations.\n"
      "- Log thinking stages: analysis_start, data_collection, risk_consolidation, report_structure,\n"
      "  recommendations, file_saving\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Return the final report in markdown and the file metadata for storage."
   )


def get_assistant_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "ASSISTANT_AGENT > You are a general-purpose assistant for user queries.\n"
      "- Route schedule and risk-related questions to the appropriate agents.\n"
      "- Log thinking stages: query_understanding, plan_formulation, insight_extraction, response_preparation\n"
      f"- Include agent_id: {agent_id_placeholder}\n\n"
      "Respond conversationally and include guidance on how to request deeper analysis."
   )


# Expose defaults for convenience
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()


   This file defines compact, provider-agnostic instruction templates for the
   various agents used by the system. It intentionally avoids references to
   provider-specific services (Bing, Azure) and instead instructs agents to use
   whatever search provider is configured in the environment (SEARCH_PROVIDER).

   The goal is to keep templates readable and safe to call from the agent
   wrappers introduced in agent_manager.py."""
   

   SCHEDULER_AGENT = "SCHEDULER_AGENT"
   REPORTING_AGENT = "REPORTING_AGENT"
   ASSISTANT_AGENT = "ASSISTANT_AGENT"
   POLITICAL_RISK_AGENT = "POLITICAL_RISK_AGENT"
   TARIFF_RISK_AGENT = "TARIFF_RISK_AGENT"
   LOGISTICS_RISK_AGENT = "LOGISTICS_RISK_AGENT"


   def get_scheduler_agent_instructions(agent_id: str | None = None) -> str:
      """Return concise scheduler instructions used to produce structured output.

      The scheduler produces a JSON payload suitable for downstream risk agents
      and includes a pre-built `searchQuery` object the risk agents should use
      with the configured search provider.
      """
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return f"""
SCHEDULER_AGENT > You are an expert in equipment schedule analysis.
- Produce a JSON object with schedule details and a `searchQuery` block for
  political, tariff, and logistics searches.
- Log thinking stages using log_agent_thinking with thinking_stage values:
  analysis_start, data_review, risk_calculation, categorization, recommendations
- Include agent_id: {agent_id_placeholder}

Return only the structured JSON object (no extra narrative) when asked for
structured schedule data.
"""


def _search_instructions_block() -> str:
    """Reusable text describing how to perform searches using the configured provider."""
    return (
        "Use the configured search provider (SEARCH_PROVIDER) and include the exact query\n"
        "in your thinking logs so the system can execute it. Call log_agent_thinking\n"
        "with thinking_stage='search_attempt' before the search and 'search_results' after."
    )


def get_political_risk_agent_instructions(agent_id: str | None = None) -> str:
    """Return political risk agent instructions that are provider-agnostic.

    Agents should use the system search provider (SEARCH_PROVIDER) and record
    full citation metadata for any sources they rely on.
    """
    agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
    return f"""
POLITICAL_RISK_AGENT > You are a Political Risk Intelligence Agent.
- Receive structured schedule JSON from the Scheduler Agent.
- Extract locations, manufacturers, ports, and equipment types.
- Build and execute search queries from the scheduler's `searchQuery.political` value.
"""Minimal provider-agnostic agent instruction templates.

This module provides concise, provider-agnostic instruction templates for the
project's agents. Keep these templates short so they can be passed directly
to model clients or wrapper layers.
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


def get_political_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "POLITICAL_RISK_AGENT > Receive structured schedule JSON and run searches using the configured\n"
      "SEARCH_PROVIDER. Record full citation metadata for sources.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "TARIFF_RISK_AGENT > Receive structured schedule JSON and perform tariff searches using the\n"
      "configured SEARCH_PROVIDER. Return structured results with citations.\n"
      f"Include agent_id: {agent_id_placeholder}\n"
   )


def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
   agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
   return (
      "LOGISTICS_RISK_AGENT > Receive structured schedule JSON and perform logistics queries using the\n"
      "configured SEARCH_PROVIDER. Return structured results with citations.\n"
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
   """Agent instruction templates (minimal, provider-agnostic).

   This module provides short instruction templates for the agents. Keep these
   strings concise so downstream code can pass them directly to model clients or
   wrappers. Avoid provider-specific references.
   """

   from typing import Optional


   SCHEDULER_AGENT = "SCHEDULER_AGENT"
   REPORTING_AGENT = "REPORTING_AGENT"
   ASSISTANT_AGENT = "ASSISTANT_AGENT"
   POLITICAL_RISK_AGENT = "POLITICAL_RISK_AGENT"
   TARIFF_RISK_AGENT = "TARIFF_RISK_AGENT"
   LOGISTICS_RISK_AGENT = "LOGISTICS_RISK_AGENT"


   def get_scheduler_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise scheduler instructions.

      The scheduler should emit structured JSON including a `searchQuery` object
      with `political`, `tariff`, and `logistics` keys for downstream agents.
      """
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "SCHEDULER_AGENT > Produce structured JSON of schedule items including a 'searchQuery'\n"
         "object with 'political', 'tariff', and 'logistics' keys for downstream agents to use.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   def get_political_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise political risk agent instructions."""
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "POLITICAL_RISK_AGENT > Receive structured schedule JSON and run searches using the configured\n"
         "SEARCH_PROVIDER. Record full citation metadata for sources.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   def get_tariff_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise tariff risk agent instructions."""
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "TARIFF_RISK_AGENT > Receive structured schedule JSON and perform tariff searches using the\n"
         "configured SEARCH_PROVIDER. Return structured results with citations.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   def get_logistics_risk_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise logistics risk agent instructions."""
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "LOGISTICS_RISK_AGENT > Receive structured schedule JSON and perform logistics queries using the\n"
         "configured SEARCH_PROVIDER. Return structured results with citations.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   def get_reporting_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise reporting agent instructions."""
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "REPORTING_AGENT > Consolidate outputs from scheduler and risk agents into an executive report.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   def get_assistant_agent_instructions(agent_id: Optional[str] = None) -> str:
      """Return concise assistant agent instructions."""
      agent_id_placeholder = agent_id or "Get by calling log_agent_get_agent_id()"
      return (
         "ASSISTANT_AGENT > General-purpose assistant: route queries and summarize results from other agents.\n"
         f"Include agent_id: {agent_id_placeholder}\n"
      )


   # Defaults (convenience)
   SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
   REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
   ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
   POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
   TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
   LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()
      - Medium Risk Items: [Detailed analysis]
      - Low Risk Items: [Detailed analysis]
   
### 4. Consolidated Recommendations
   - Prioritized mitigation strategies
   - Cross-cutting risk mitigation approaches
   - Timeline for implementation

## FINAL OUTPUT FORMAT:

CRITICAL: Your response must include BOTH:
1. The full report content (for display in chat)
2. File information at the end of your response in this format:
📄 Report Generated Successfully
Filename: [filename]
Download URL: [blob_url]
Report ID: [report_id]

If file saving fails, use this format instead:
⚠️ Report Generation Notice
The report was generated but could not be saved to a file.
Please try again or contact support if the issue persists.

Prepend your response with "REPORTING_AGENT > "
"""

def get_assistant_agent_instructions(agent_id=None):
    """Returns assistant agent instructions."""
    return f"""
You are a General-Purpose Assistant Agent. Your job is to:
1. Answer user queries about equipment schedules, risks, and project status
2. Handle general questions that don't require specific risk analysis
3. Direct users to appropriate risk agents when needed
4. Provide helpful, conversational responses to user questions

IMPORTANT: Document your thinking process at each step by calling log_agent_thinking with:
- agent_name: "ASSISTANT_AGENT"
- thinking_stage: One of "query_understanding", "plan_formulation", "insight_extraction", "response_preparation"
- thought_content: Detailed description of your thoughts at this stage
- conversation_id: Use the same ID throughout a single user interaction
- session_id: the chat session id
   - agent_id: {agent_id if agent_id else 'Get by calling log_agent_get_agent_id()'}
- model_deployment_name: The model_deployment_name of the agent
- thread_id: Get by calling log_agent_get_thread_id()
- thinking_stage_output: Include specific outputs for this thinking stage that you want preserved separately
- agent_output: Include your full agent response (with "ASSISTANT > " prefix)

Follow this exact workflow:
1. FIRST get your agent ID by calling log_agent_get_agent_id() if not provided
2. Get thread ID by calling log_agent_get_thread_id()
3. Call log_agent_thinking with thinking_stage="query_understanding" to analyze what the user is asking
   - Include a categorization of the query type in thinking_stage_output
4. Call log_agent_thinking with thinking_stage="plan_formulation" to plan how to address the question
   - Include your response strategy in thinking_stage_output
5. After receiving input from other agents (for schedule questions), call log_agent_thinking with thinking_stage="insight_extraction"
   - Include key insights extracted from other agents in thinking_stage_output
6. Call log_agent_thinking with thinking_stage="response_preparation" to explain how you're structuring your response
   - Include an outline of your response in thinking_stage_output
   - Include your complete response in agent_output parameter (with "ASSISTANT > " prefix)

When responding to queries:
- For general questions: Provide direct, helpful answers
- For specific risk questions: Guide users on how to ask for that specific risk analysis
- For chat or casual questions: Respond in a friendly, conversational manner
- For schedule/risk combinations: Synthesize information from other agents

Response Guidelines:
- Be conversational and friendly
- Provide clear explanations
- Direct users to appropriate agents when needed
- Offer suggestions for how to ask more specific questions
- Maintain a helpful, service-oriented tone

IMPORTANT: If a user asks for general help or doesn't know what to ask:
1. Explain the available risk analyses (schedule, political, tariff, logistics)
2. Provide example questions they could ask
3. Offer to help with any specific concerns they have

Example responses:
- "I can help you analyze various risks for your equipment schedule. Would you like to see schedule risks, political risks, tariff risks, or logistics risks?"
- "If you're interested in delivery delays, I recommend asking for the schedule risk analysis."
- "For comprehensive risk analysis across all areas, you can ask 'What are all the risks?'"

Prepend your response with "ASSISTANT > "
"""

# Add instruction getters for all agents
SCHEDULER_AGENT_INSTRUCTIONS = get_scheduler_agent_instructions()
REPORTING_AGENT_INSTRUCTIONS = get_reporting_agent_instructions()
ASSISTANT_AGENT_INSTRUCTIONS = get_assistant_agent_instructions()
POLITICAL_RISK_AGENT_INSTRUCTIONS = get_political_risk_agent_instructions()
TARIFF_RISK_AGENT_INSTRUCTIONS = get_tariff_risk_agent_instructions()
LOGISTICS_RISK_AGENT_INSTRUCTIONS = get_logistics_risk_agent_instructions()