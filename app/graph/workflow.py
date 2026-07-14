from langgraph.graph import StateGraph, START, END
from app.graph.state import JobPipelineState
from app.graph.nodes.jd_parser_agent import parse_job_description
from app.services.vector_db import add_job_to_vector_db


def node_parse_job(state: JobPipelineState):
    print(f"\n[Graph] Parsing job {state['job_id']}...")

    parsed = parse_job_description(state["raw_text"])

    return {"parsed_jd": parsed}

def node_add_to_vector_db(state: JobPipelineState):
    print(f"[Graph] Adding job {state['job_id']} to Vector DB...")

    job_string = state["parsed_jd"].model_dump_json() 

    add_job_to_vector_db(job_id=state["job_id"], job_text=job_string)

    return {}


workflow = StateGraph(JobPipelineState)

workflow.add_node("parse_node", node_parse_job)
workflow.add_node("vector_node", node_add_to_vector_db)

workflow.set_entry_point("parse_node")
workflow.add_edge("parse_node", "vector_node")
workflow.add_edge("vector_node", END)

app_graph = workflow.compile()

