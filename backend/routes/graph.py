"""
GET /api/graph — Knowledge graph data
"""
from fastapi import APIRouter
from knowledge_graph import get_knowledge_graph
from models import GraphData

router = APIRouter()


@router.get("/graph", response_model=GraphData)
async def get_graph():
    """Return knowledge graph data for visualization."""
    return get_knowledge_graph()
