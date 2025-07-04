# PR Content Generator

A Python tool that generates pull request descriptions using OpenAI's GPT models based on git changes and customizable templates.

## Features

- Generate PR descriptions based on git commits and diffs
- Use customizable templates for consistent PR formatting
- Leverage OpenAI's GPT models for intelligent content generation
- Compare against any base branch
- Include extensive git diff context for better analysis

## Prerequisites

- Python 3.7+
- Git repository
- OpenAI API key

## Installation

1. Clone or download this repository
2. Set up a Python virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install openai
   ```

## Setup

1. Get an OpenAI API key from [OpenAI's website](https://platform.openai.com/api-keys)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.) for persistence.

## Usage

```bash
python gen_pr.py <template_file> <base_branch>
```

### Arguments

- `template_file`: Name of the template file (stored in the same directory as the script)
- `base_branch`: The base branch to compare against (e.g., `main`, `develop`, `master`)

### Examples

```bash
# Generate PR content using a standard template, comparing against main branch
python gen_pr.py standard_template.md main

# Generate PR content using a feature template, comparing against develop branch
python gen_pr.py feature_template.md develop
```

## Templates

Templates are text files that define the structure of your PR description. They should be placed in the same directory as the `gen_pr.py` script.

### Example Template (`standard_template.md`)

```markdown
## Summary
[Brief description of changes]

## Changes Made
- [List of key changes]

## Testing
- [How the changes were tested]

## Impact
- [Any potential impact or breaking changes]

## Additional Notes
[Any additional context or notes]
```

### Template Guidelines

- Use clear section headers
- Include placeholders or guidance text in brackets
- Keep the template structure consistent with your team's standards
- The AI will fill in the template based on your git changes and commit messages

## How It Works

1. **Git Analysis**: The tool runs `git log` and `git diff` to gather information about changes between your current branch and the base branch
2. **Template Loading**: Loads your specified template file
3. **AI Generation**: Sends the template, git log, and diff to OpenAI's GPT model
4. **Output**: Returns a formatted PR description based on your template and changes

## Configuration

The tool uses the following git commands:
- `git log {base_branch}..HEAD --oneline --no-merges` - Gets commit messages
- `git diff {base_branch}..HEAD -U10000` - Gets detailed diff with extensive context

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not set in environment"**
   - Make sure you've exported the `OPENAI_API_KEY` environment variable
   - Check that the API key is valid and has sufficient credits

2. **Template file not found**
   - Ensure the template file is in the same directory as `gen_pr.py`
   - Check the filename spelling and extension

3. **Git command failures**
   - Make sure you're in a git repository
   - Verify the base branch exists and is accessible
   - Ensure you have commits to compare (your branch is ahead of the base branch)

### Environment Variables

- `OPENAI_API_KEY`: Required. Your OpenAI API key for accessing GPT models.

## License

This tool is provided as-is for educational and development purposes.
