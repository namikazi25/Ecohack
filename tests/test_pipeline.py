import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from backend.agents.planner import PlanningAgent
from backend.agents.evaluator import EvaluatingAgent
from backend.agents.executor import ExecutingAgent

@pytest.fixture
def planner():
    return PlanningAgent()

@pytest.fixture
def evaluator():
    return EvaluatingAgent()

@pytest.fixture
def executor():
    return ExecutingAgent()

def test_full_pipeline(planner, evaluator, executor):
    """Test full agent pipeline for a text query."""
    query = "Tell me about the Red Fox."
    
    for attempt in range(3):
        plan = planner.plan(query)
        evaluation = evaluator.evaluate(plan)

        if "error" not in evaluation:
            response = executor.execute(evaluation)
            assert "response" in response, "Final execution should return a response"
            assert len(response["response"]) > 0, "Response should not be empty"
            break  # Stop retrying if successful
