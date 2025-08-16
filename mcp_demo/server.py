from mcp.server.fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP("MCP Demo", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name='Say Hello',
    description='Say hello to the user'
)
def say_hello(name: str = Field(description="Name of the user")):
    return f"Hello {name}!"

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="application/json"
)
def read_resource(doc_id: str = Field(description="id of the document to read. For example: plan.md OR report.pdf")):
    return docs[doc_id]

mcp_app = mcp.streamable_http_app()