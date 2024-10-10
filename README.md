
# Scribe: AI-Powered Code Writing Assistant

Scribe is a powerful command-line interface (CLI) tool designed to assist developers in writing and modifying code using artificial intelligence (claude 3.5 sonnet LLM). It leverages advanced language models to generate, edit, and explain code based on user prompts and existing codebases.

## Features

- **Single File Writing**: Easily modify or generate code for a single file with AI assistance.
- **Multi-File Writing**: Update multiple files simultaneously, maintaining consistency across your project.
- **Project Initialization**: Quickly set up your project with Scribe configuration.
- **Reference Support**: Include other files as context for more accurate code generation.
- **Interactive GUI**: Review and accept AI-generated changes through a user-friendly interface.

## Installation

(Add installation instructions here)

## Usage
### Setup your Anthropic key to interact with claude-3.5

```bash
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_KEY
```

### Initialize a Project

```bash
scribe init
```

This command sets up the Scribe configuration for your project, creating a `scribeconfig` directory and updating your `.gitignore` file.

### Write to a Single File

```bash
scribe write <file_path> --prompt "Your instruction" --references <reference_files>
```

Modify or generate code in a specific file based on your prompt and optional reference files.

### Write to Multiple Files

```bash
scribe multi-write <file_path1> <file_path2> ... --prompt "Your instruction" --references <reference_files>
```

Update multiple files in one go, maintaining consistency across your codebase.

## How It Works

Scribe is an agent that sits between an LLM (currently claude) and your codebase. It considers the context of your existing code and any provided references to ensure the generated code fits seamlessly into your project.

