# MCDA Model Context Protocol (MCP) Server

This project implements a Model Context Protocol (MCP) server for Multi-Criteria Decision Analysis (MCDA) applications.

It provides tools to interact with an internal database (Python API) that serves as a source for MCDA decision data.  
The server exposes structured tools through the MCP interface, allowing seamless integration with LLMs, AI agents, or other compatible clients.

## Project Structure

- **mcda_mcp.py**  
  Sets up the MCP server using `FastMCP`.  
  Defines tools for:

  - Checking available MCDA processes
  - Retrieving process-specific data

- **mcda_client.py**  
  Provides an asynchronous HTTP client for interacting with the MCDA backend API.  
  Handles all network operations and error management.

## Purpose

This MCP server serves as a bridge between an MCDA-focused backend API and Model Context Protocol clients, enabling structured decision support operations through an AI-native interface.
