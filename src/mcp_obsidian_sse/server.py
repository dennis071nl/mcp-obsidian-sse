import logging
import os
import json
from collections.abc import Sequence
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from .obsidian import Obsidian

load_dotenv()

# Configure the logging
log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger("mcp-obsidian")

API_KEY = os.getenv("OBSIDIAN_API_KEY")
if not API_KEY:
    raise ValueError(f"OBSIDIAN_API_KEY environment variable required. Working directory: {os.getcwd()}")

mcp = FastMCP('mcp-obsidian-sse')

@mcp.tool(
    name="obsidian_list_files_in_vault",
    description="""Lists all files and directories in the root directory of your Obsidian vault.

    Args:
        None
    """,
)
def list_files_in_vault_tool_handler() -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    files = api.list_files_in_vault()

    return [
        TextContent(
            type="text",
            text=json.dumps(files, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_list_files_in_dir",
    description="""Lists all files and directories that exist in a specific Obsidian directory.

    Args:
        dirpath: string - Path to list files from (relative to your vault root). Note that empty directories will not be returned.
    """,
)
def list_files_in_dir_tool_handler(dirpath: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    files = api.list_files_in_dir(dirpath)

    return [
        TextContent(
            type="text",
            text=json.dumps(files, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_get_file_contents",
    description="""Return the content of a single file in your vault.

    Args:
        filepath: string - Path to the relevant file (relative to your vault root).
    """,
)
def get_file_contents_tool_handler(filepath: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    content = api.get_file_contents(filepath)

    return [
        TextContent(
            type="text",
            text=json.dumps(content, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_simple_search",
    description="""Simple search for documents matching a specified text query across all files in the vault.
    Use this tool when you want to do a simple text search.

    Args:
        query: string - Text to a simple search for in the vault.
        context_length: int - How much context to return around the matching string (default: 100)
    """,
)
def search_tool_handler(query: str, context_length: int = 100) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    results = api.search(query, context_length)

    formatted_results = []
    for result in results:
        formatted_matches = []
        for match in result.get('matches', []):
            context = match.get('context', '')
            match_pos = match.get('match', {})
            start = match_pos.get('start', 0)
            end = match_pos.get('end', 0)

            formatted_matches.append({
                'context': context,
                'match_position': {'start': start, 'end': end}
            })

        formatted_results.append({
            'filename': result.get('filename', ''),
            'score': result.get('score', 0),
            'matches': formatted_matches
        })

    return [
        TextContent(
            type="text",
            text=json.dumps(formatted_results, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_append_content",
    description="""Append content to a new or existing file in the vault.

    Args:
        filepath: string - Path to the relevant file (relative to your vault root).
        content: string - Content to append to the file.
    """,
)
def append_content_tool_handler(filepath: str, content: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    api.append_content(filepath, content)

    return [
        TextContent(
            type="text",
            text=f"Successfully appended content to {filepath}."
        )
    ]

@mcp.tool(
    name="obsidian_patch_content",
    description="""Insert content into an existing note relative to a heading, block reference, or frontmatter field.

    Args:
        filepath: string - Path to the relevant file (relative to your vault root).
        operation: string - Operation to perform (append, prepend, or replace).
        target_type: string - Type of target to patch (heading, block, or frontmatter).
        target: string - Target Identifier (heading path, block reference, or frontmatter field).
        content: string - Content to insert into the file.
    """,
)
def patch_content_tool_handler(filepath: str, operation: str, target_type: str, target: str, content: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    api.patch_content(filepath, operation, target_type, target, content)

    return [
        TextContent(
            type="text",
            text=f"Successfully patched content in {filepath}."
        )
    ]

@mcp.tool(
    name="obsidian_delete_file",
    description="""Delete a file or directory from the vault.

    Args:
        filepath: string - Path to the file or directory to delete (relative to vault root).
        confirm: boolean - Confirmation to delete the file (must be true).
    """,
)
def delete_file_tool_handler(filepath: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    api.delete_file(filepath)

    return [
        TextContent(
            type="text",
            text=f"Successfully deleted {filepath}."
        )
    ]

@mcp.tool(
    name="obsidian_complex_search",
    description="""Complex search for documents using a JsonLogic query.
    Supports standard JsonLogic operators plus 'glob' and 'regexp' for pattern matching. Results must be non-falsy.

    Use this tool when you want to do a complex search, e.g. for all documents with certain tags etc.

    Args:
        query: string - JsonLogic query object. Example: {\"glob\": [\"*.md\", {\"var\": \"path\"}]} matches all markdown files.
    """,
)
def complex_search_tool_handler(query: str) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    results = api.search_json(query)

    return [
        TextContent(
            type="text",
            text=json.dumps(results, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_batch_get_file_contents",
    description="""Return the contents of multiple files in your vault, concatenated with headers.

    Args:
        filepaths: list of strings - Paths to the files to get contents from (relative to vault root).
    """,
)
def batch_get_file_contents_tool_handler(filepaths: list[str]) -> Sequence[TextContent]:
    api = Obsidian(api_key=API_KEY)
    contents = api.batch_get_file_contents(filepaths)

    return [
        TextContent(
            type="text",
            text=json.dumps(contents, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_get_periodic_notes",
    description="""Get current periodic note for the specified period.

    Args:
        period: string - Period to get the periodic note for (e.g. 'daily', 'weekly', 'monthly', 'quarterly', 'yearly').
    """,
)
def get_periodic_notes_tool_handler(period: str) -> Sequence[TextContent]:
    valid_periods = ['daily', 'weekly', 'monthly', 'quarterly', 'yearly']

    if period not in valid_periods:
        raise ValueError(f"Invalid period: {period}. Valid periods are: {', '.join(valid_periods)}")

    api = Obsidian(api_key=API_KEY)
    note = api.get_periodic_note(period)

    return [
        TextContent(
            type="text",
            text=json.dumps(note, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_get_recent_periodic_notes",
    description="""Get recent periodic notes for the specified period type.

    Args:
        period: string - Period to get the recent periodic notes for (e.g. 'daily', 'weekly', 'monthly', 'quarterly', 'yearly').
        limit: int - Maximum number of recent periodic notes to return (default: 10).
        include_content: boolean - Whether to include the content of the periodic notes (default: false).
    """,
)
def get_recent_periodic_notes_tool_handler(period: str, limit: int = 10, include_content: bool = False) -> Sequence[TextContent]:
    valid_periods = ['daily', 'weekly', 'monthly', 'quarterly', 'yearly']

    if period not in valid_periods:
        raise ValueError(f"Invalid period: {period}. Valid periods are: {', '.join(valid_periods)}")

    limit = min(limit, 100)
    limit = max(limit, 1)

    api = Obsidian(api_key=API_KEY)
    notes = api.get_recent_periodic_notes(period, limit, include_content)

    return [
        TextContent(
            type="text",
            text=json.dumps(notes, indent=4)
        )
    ]

@mcp.tool(
    name="obsidian_get_recent_changes",
    description="""Get recently modified files in the vault.

    Args:
        limit: int - Maximum number of recent changes to return (default: 10).
        days: int - Number of days to look back for changes (default: 90).
    """,
)
def get_recent_changes_tool_handler(limit: int = 10, days: int = 90) -> Sequence[TextContent]:
    limit = min(limit, 100)
    limit = max(limit, 1)
    days = min(days, 365)
    days = max(days, 1)

    api = Obsidian(api_key=API_KEY)
    changes = api.get_recent_changes(limit, days)

    return [
        TextContent(
            type="text",
            text=json.dumps(changes, indent=4)
        )
    ]
