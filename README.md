# Sample Project

A modern Python CLI tool template with best practices.

## Features

- 🚀 Modern Python packaging with `pyproject.toml`
- ✅ Testing with pytest
- 🔧 CI/CD with GitHub Actions
- 📦 Type hints support
- 🎨 Code formatting with black

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Run the CLI
sample-cli --help

# Greet someone
sample-cli greet Alice
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI
├── src/
│   └── sample_project/     # Main package
│       ├── __init__.py
│       └── cli.py
├── tests/
│   └── test_cli.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## License

MIT License
