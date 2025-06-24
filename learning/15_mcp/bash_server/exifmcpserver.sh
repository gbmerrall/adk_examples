#!/bin/bash
# EXIF data retrieval implementation

# Override configuration paths BEFORE sourcing the core
MCP_CONFIG_FILE="$(dirname "${BASH_SOURCE[0]}")/assets/exifserver_config.json"
MCP_TOOLS_LIST_FILE="$(dirname "${BASH_SOURCE[0]}")/assets/exifserver_tools.json"
MCP_LOG_FILE="$(dirname "${BASH_SOURCE[0]}")/logs/exifserver.log"

# MCP Server Tool Function Guidelines:
# 1. Name all tool functions with prefix "tool_" followed by the same name defined in tools_list.json
# 2. Function should accept a single parameter "$1" containing JSON arguments
# 3. For successful operations: Echo the expected result and return 0
# 4. For errors: Echo an error message and return 1
# 5. All tool functions are automatically exposed to the MCP server based on tools_list.json

# Source the core MCP server implementation
source "$(dirname "${BASH_SOURCE[0]}")/mcpserver_core.sh"

# Tool: Get EXIF data for a file
# Parameters: Takes a JSON object with filename
# Success: Echo JSON result and return 0
# Error: Echo error message and return 1
tool_get_exif() {
    local args="$1"
    local filename=$(echo "$args" | jq -r '.filename')
    
    # Parameter validation
    if [[ -z "$filename" ]]; then
        echo "Missing required parameter: filename"
        return 1
    fi

    # Hardcoded directory
    local exif_dir="${HOME}/Pictures/exif"
    local file_path="${exif_dir}/${filename}"

    # Check if file exists
    if [[ ! -f "$file_path" ]]; then
        echo "File not found: ${filename}"
        return 1
    fi
    
    # Use exiftool to get EXIF data in JSON format
    local exif_data=$(exiftool -json "$file_path")
    echo "$exif_data"
    return 0
}

# Start the MCP server
run_mcp_server "$@" 