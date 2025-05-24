# MCDA Model Context Protocol (MCP) Server

This project implements a Model Context Protocol (MCP) server for Multi-Criteria Decision Analysis (MCDA) applications.

It provides tools to interact with an internal database (Python API) that serves as a source for MCDA decision data.  
The server exposes structured tools through the MCP interface, allowing seamless integration with LLMs, AI agents, or other compatible clients.

## Available Functions

The following MCP tools are available for multi-criteria decision analysis (MCDA).

### PROMETHEE Methods

These tools implement the PROMETHEE (Preference Ranking Organization Method for Enrichment Evaluations) family of algorithms for ranking alternatives based on multiple criteria.

1. **`promethee_1`**

   - **Description**: Computes partial ranking using positive (entering) and negative (leaving) flows.
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `positive_flows`: List of positive flow scores.
     - `negative_flows`: List of negative flow scores.
     - `error`: Error message if the computation fails.

2. **`promethee_2`**

   - **Description**: Computes complete ranking using net flows (positive - negative).
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `net_flows`: List of net flow scores.
     - `error`: Error message if the computation fails.

3. **`promethee_3`**

   - **Description**: Computes ranking with intervals to account for uncertainty, using net flows and an alpha parameter.
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `intervals`: List of tuples (net_flow, lower_bound, upper_bound).
     - `error`: Error message if the computation fails.

4. **`promethee_4`**

   - **Description**: Computes normalized net flows for a continuous case (simplified for discrete alternatives).
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `normalized_flows`: List of normalized net flow scores.
     - `error`: Error message if the computation fails.

5. **`promethee_5`**

   - **Description**: Computes net flows with constraints to filter feasible alternatives.
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `constrained_flows`: List of net flows (None for infeasible alternatives).
     - `error`: Error message if the computation fails.

6. **`promethee_6`**
   - **Description**: Computes min, central, and max flows to model hesitation in decision-making.
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `min_flows`: List of minimum flow scores.
     - `central_flows`: List of central flow scores.
     - `max_flows`: List of maximum flow scores.
     - `error`: Error message if the computation fails.

### AHP Method

This tool implements the Analytic Hierarchy Process (AHP) for deriving priorities and ranking alternatives based on pairwise comparison matrices.

1. **`ahp`**
   - **Description**: Computes criteria weights and alternative scores using pairwise comparison matrices, with optional consistency checks.
   - **Output**: Dictionary containing:
     - `alternatives`: List of alternative names.
     - `criteria`: List of criterion names.
     - `criteria_weights`: List of weights for each criterion.
     - `alternative_scores`: List of final scores for each alternative.
     - `consistency_info`: Dictionary with consistency ratios for criteria and alternatives matrices.
     - `error`: Error message if the computation fails.

## Notes

- PROMETHEE methods support various preference functions (e.g., 'usual', 'u_shape', 'v_shape', 'level', 'linear', 'gaussian').
- AHP includes consistency checks to validate pairwise comparison matrices, using a default threshold of 0.1.

## Purpose

This MCP server serves as a bridge between an MCDA-focused backend API and Model Context Protocol clients, enabling structured decision support operations through an AI-native interface.
