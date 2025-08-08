from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", stateless_http=True)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc

@mcp.tool(
    name="read_document",
    description="Read the contents of the document"
)
def read_document(doc_id: str = Field(description="The ID of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")
    return docs[doc_id]

# TODO: Write a tool to edit a doc

@mcp.tool(
    name="edit_document",
    description="Edit the contents of the document. Replace the the older content with the new content then return the new content"
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit"),
    old_content: str = Field(description="Old content from the document to replace."),
    new_content: str = Field(description="New content to put in place of the old content.")):

    if doc_id not in docs:
        raise ValueError(f"Document {doc_id} not found")

    if old_content not in docs[doc_id]:
        raise ValueError(f"Old content {old_content} not found in document {doc_id}")

    docs[doc_id] = docs[doc_id].replace(old_content, new_content)
    return docs[doc_id]


# TODO: Write a resource to return all doc id's
# TODO: Write a resource to return the contents of a particular doc
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc

mcp_app = mcp.streamable_http_app()