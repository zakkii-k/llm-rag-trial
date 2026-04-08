#!/bin/bash
# MCP サーバー起動スクリプト
# mcp パッケージが未インストールの場合のみインストールして起動する

set -e

pip install mcp --quiet --disable-pip-version-check 2>/dev/null

exec python "$(dirname "$0")/mcp_server.py"
