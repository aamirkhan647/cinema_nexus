"""Non-mock unit tests verifying agent topology, tools, configuration, and callbacks."""

import pytest

from agent import root_agent
from agents import (
    critic_agent,
    director_agent,
    recommender_agent,
    watchlist_agent,
)
from config import (
    CRITIC_MAX_TOKENS,
    CRITIC_TEMPERATURE,
    MODEL_NAME,
    RECOMMENDER_MAX_TOKENS,
    RECOMMENDER_TEMPERATURE,
    WATCHLIST_MAX_TOKENS,
    WATCHLIST_TEMPERATURE,
)
from safety.callbacks import (
    input_guardrail,
    output_guardrail,
    watchlist_tool_guardrail,
)
from tools.mcp_toolsets import fetch_toolset
from tools.watchlist_ops import manage_watchlist


class TestAgentTopologyAndConfiguration:
    def test_root_agent_identity(self):
        assert root_agent is director_agent
        assert director_agent.name == "CinemaNexusDirector"
        assert director_agent.model == MODEL_NAME

    def test_director_agent_sub_agents_and_callbacks(self):
        sub_agent_names = [a.name for a in director_agent.sub_agents]
        assert "CriticAgent" in sub_agent_names
        assert "RecommenderAgent" in sub_agent_names
        assert "WatchlistAgent" in sub_agent_names

        assert director_agent.before_model_callback is input_guardrail
        assert director_agent.after_model_callback is output_guardrail
        assert "cinema_nexus" in director_agent.global_instruction.lower()

    def test_critic_agent_configuration(self):
        assert critic_agent.name == "CriticAgent"
        assert critic_agent.output_key == "last_review"
        assert fetch_toolset in critic_agent.tools

        config = critic_agent.generate_content_config
        assert config.temperature == CRITIC_TEMPERATURE
        assert config.max_output_tokens == CRITIC_MAX_TOKENS

    def test_recommender_agent_configuration(self):
        assert recommender_agent.name == "RecommenderAgent"
        assert "{user_watchlist?}" in recommender_agent.instruction
        assert fetch_toolset in recommender_agent.tools

        config = recommender_agent.generate_content_config
        assert config.temperature == RECOMMENDER_TEMPERATURE
        assert config.max_output_tokens == RECOMMENDER_MAX_TOKENS

    def test_watchlist_agent_configuration(self):
        assert watchlist_agent.name == "WatchlistAgent"
        assert manage_watchlist in watchlist_agent.tools
        assert watchlist_agent.before_tool_callback is watchlist_tool_guardrail

        config = watchlist_agent.generate_content_config
        assert config.temperature == WATCHLIST_TEMPERATURE
        assert config.max_output_tokens == WATCHLIST_MAX_TOKENS
