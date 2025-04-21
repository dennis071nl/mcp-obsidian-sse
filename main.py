from starlette.applications import Starlette
from starlette.routing import Mount
from mcp_obsidian_sse import mcp

app = Starlette(
    routes=[
        Mount("/", app=mcp.sse_app()),
    ]
)