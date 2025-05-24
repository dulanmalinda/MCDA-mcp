import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Tuple

from mcda_db import MCDADatabaseClient

from Ranking_Functions.mcda_promethee_calc import MCDACalcPromethee
from Ranking_Functions.mcda_ahp_calc import MCDACalcAHP

mcp = FastMCP("MCDA_MCP")

# DATABASE RELATED
mcda_db_client = MCDADatabaseClient()
@mcp.tool()
async def check_data_availability() -> Dict[str, Any]:
    """
    Checks the DB whether particular process data are available or not.

    Parameters:
    - None

    Returns:
    - Dictionary containing either available data or an error message.
    """
    return await mcda_db_client.check_data_availability()

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
    return await mcda_db_client.get_process_data(input_data.process)
# END


# PROMETHEE CALCULATIONS RELATED
class PrometheeInput(BaseModel):
    alternatives: List[str] = Field(description="List of alternative names.")
    criteria: List[str] = Field(description="List of criterion names.")
    weights: List[float] = Field(description="List of weights for each criterion.")
    evaluations: List[List[float]] = Field(description="Matrix of evaluations: evaluations[i][j] for alternative i on criterion j.")
    maximize: List[bool] = Field(default=None, description="List of booleans indicating if each criterion is maximized (True) or minimized (False).")
    preference_functions: Optional[List[str]] = Field(default=None, description="List of preference functions for each criterion (e.g., 'usual', 'linear').")
    thresholds: Optional[List[Tuple[float, float, float]]] = Field(default=None, description="List of (q, p, s) thresholds for each criterion.")
    alpha: Optional[float] = Field(default=0.1, description="Alpha parameter for PROMETHEE III.")
    constraints: Optional[List[bool]] = Field(default=None, description="Constraints for PROMETHEE V (True if feasible).")

@mcp.tool()
async def promethee_1(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE I algorithm for partial ranking with positive and negative flows.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing positive and negative flows or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        pos_flows, neg_flows = mcda.promethee_1(input_data.preference_functions, input_data.thresholds)
        return {
            "alternatives": input_data.alternatives,
            "positive_flows": pos_flows,
            "negative_flows": neg_flows
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def promethee_2(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE II algorithm for complete ranking with net flows.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing net flows or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        net_flows = mcda.promethee_2(input_data.preference_functions, input_data.thresholds)
        return {
            "alternatives": input_data.alternatives,
            "net_flows": net_flows
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def promethee_3(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE III algorithm for ranking with intervals.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing net flows with intervals or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        intervals = mcda.promethee_3(input_data.preference_functions, input_data.thresholds, input_data.alpha)
        return {
            "alternatives": input_data.alternatives,
            "intervals": intervals
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def promethee_4(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE IV algorithm for normalized net flows.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing normalized net flows or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        norm_flows = mcda.promethee_4(input_data.preference_functions, input_data.thresholds)
        return {
            "alternatives": input_data.alternatives,
            "normalized_flows": norm_flows
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def promethee_5(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE V algorithm with constraints.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing constrained net flows or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        constrained_flows = mcda.promethee_5(input_data.preference_functions, input_data.thresholds, input_data.constraints)
        return {
            "alternatives": input_data.alternatives,
            "constrained_flows": constrained_flows
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
async def promethee_6(input_data: PrometheeInput) -> dict[str, Any]:
    """
    Runs PROMETHEE VI algorithm for min, central, and max flows.

    Parameters:
    - input_data: PrometheeInput model with alternatives, criteria, weights, evaluations, and optional parameters.

    Returns:
    - Dictionary containing min, central, and max flows or an error message.
    """
    try:
        mcda = MCDACalcPromethee(
            alternatives=input_data.alternatives,
            criteria=input_data.criteria,
            weights=input_data.weights,
            evaluations=input_data.evaluations,
            maximize=input_data.maximize if input_data.maximize is not None else True
        )
        min_flows, central_flows, max_flows = mcda.promethee_6(input_data.preference_functions, input_data.thresholds)
        return {
            "alternatives": input_data.alternatives,
            "min_flows": min_flows,
            "central_flows": central_flows,
            "max_flows": max_flows
        }
    except Exception as e:
        return {"error": str(e)}
# END



# AHP CALCULATIONS RELATED

class AHPInput(BaseModel):
    alternatives: List[str] = Field(description="List of alternative names.")
    criteria: List[str] = Field(description="List of criterion names.")
    criteria_matrix: List[List[float]] = Field(description="Pairwise comparison matrix for criteria.")
    alternatives_matrices: List[List[List[float]]] = Field(description="List of pairwise comparison matrices for alternatives per criterion.")
    check_consistency: Optional[bool] = Field(default=True, description="Whether to check consistency of matrices.")
    consistency_threshold: Optional[float] = Field(default=0.1, description="Maximum acceptable consistency ratio.")

@mcp.tool()
async def ahp(input_data: AHPInput) -> dict[str, Any]:
    """
    Runs AHP algorithm to compute priorities and final scores.

    Parameters:
    - input_data: AHPInput model with alternatives, criteria, pairwise comparison matrices, and optional parameters.

    Returns:
    - Dictionary containing criteria weights, alternative scores, consistency info, or an error message.
    """
    try:
        ahp = MCDACalcAHP(
            criteria=input_data.criteria,
            alternatives=input_data.alternatives,
            criteria_matrix=input_data.criteria_matrix,
            alternatives_matrices=input_data.alternatives_matrices
        )
        criteria_weights, alternative_scores, consistency_info = ahp.compute_ahp(
            check_consistency=input_data.check_consistency,
            consistency_threshold=input_data.consistency_threshold
        )
        return {
            "alternatives": input_data.alternatives,
            "criteria": input_data.criteria,
            "criteria_weights": criteria_weights,
            "alternative_scores": alternative_scores,
            "consistency_info": consistency_info
        }
    except Exception as e:
        return {"error": str(e)}
    
# END
