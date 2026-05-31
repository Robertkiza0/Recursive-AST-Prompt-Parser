# Recursive-AST-Prompt-Parser
A specialized script parsing tool designed to optimize token consumption for LLM-based coding agents.
# AST Prompt Parser for LLM Context Windows

A specialized script parsing tool designed to optimize token consumption for LLM-based coding agents.

## Features
- Leverages Python's native Abstract Syntax Tree (`ast`) module to walk through code architecture.
- Recursively extracts high-level structural topology (Class definitions, method signatures, arguments).
- Filters out verbose execution logic to feed highly compressed blueprints into Large Language Model context windows.
