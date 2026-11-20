"""
CinemaNexus - MCP Toolsets
==========================
External MCP server tool integrations.
"""

# Ensure central configuration & shims are initialized
try:
    from ..config import MCP_FETCH_TIMEOUT
except (ImportError, ValueError):
    from config import MCP_FETCH_TIMEOUT

from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# MCP Toolset: mcp-server-fetch for live web content retrieval
fetch_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="uvx",
            args=["mcp-server-fetch", "--ignore-robots-txt", "--no-readability-js"],
        ),
        timeout=MCP_FETCH_TIMEOUT,
    ),
)
