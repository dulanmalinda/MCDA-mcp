import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any

from mcda_client import MCDAClient

mcp = FastMCP("MCDA_MCP")

mcda_client = MCDAClient()

@mcp.tool()
async def check_data_availability() -> Dict[str, Any]:
    """
    Checks the DB whether particular process data are available or not.

    Parameters:
    - None

    Returns:
    - Dictionary containing either available data or an error message.
    """
    return await mcda_client.check_data_availability()

class ProcessInput(BaseModel):
    process: str = Field(description="Process name exactly as received from check_data_availability.")

@mcp.tool()
async def get_process_data(input_data: ProcessInput) -> Dict[str, Any]:
    """
    Retrieves data for a particular process.

    Parameters:
    - input_data: A ProcessInput model containing the process name.

    Returns:
    - Dictionary containing the specified process data or an error message.
    """
    return await mcda_client.get_process_data(input_data.process)
