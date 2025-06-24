To make this super simple we're going to use a bash MCP server. 
See https://github.com/muthuishere/mcp-server-bash-sdk

Once you've checked out the bash server copy the contents of the 'bash_server' directory over 
ensuring the two tools in the 'tools' directory go into the tools directory for the MCP server.

The tool is an exif image checker that looks in ~/Pictures/exif/ and extracts exif into using exiftool (make sure it's installed). 
If you request the GPS info you can also ask for a Google Maps link.