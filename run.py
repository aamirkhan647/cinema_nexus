"""cinema_nexus - CLI Runner
Bypasses the Windows symlink privilege restriction in `adk run` and mutes noisy SDK warnings.
"""

import asyncio
import logging
import os
import sys
import warnings

# Suppress experimental and non-critical UserWarnings from ADK
warnings.filterwarnings("ignore", category=UserWarning)

# Suppress noisy warning logs from Google GenAI SDK and ADK internal tools
logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("google.adk").setLevel(logging.ERROR)

from google.adk.cli.cli import run_cli

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    agent_name = os.path.basename(current_dir)

    save_session = "--save_session" in sys.argv

    asyncio.run(
        run_cli(
            agent_parent_dir=parent_dir,
            agent_folder_name=agent_name,
            save_session=save_session,
        )
    )
