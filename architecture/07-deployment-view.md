# Chapter 7: Deployment View

## 7.1 Overview

This is a kata with no deployment target. The system runs as a single Python
process on the developer's local machine, invoked either by pytest or directly
from a Python REPL. There is no server, no container, no cloud infrastructure.

```
Developer's machine
└── Python 3.12 interpreter
    └── social_network/          ← single process
        ├── posting/
        ├── social_graph/
        ├── timeline/
        └── messaging/
```

## 7.2 Execution Environments

| Environment | How it's run | Persistence |
|-------------|-------------|-------------|
| **Test** | `pytest` | In-memory only; each test starts with fresh repository instances. |
| **Local REPL / script** | `python -m social_network ...` (if a CLI is added) | In-memory only; state is lost when the process exits. |

## 7.3 Infrastructure Requirements

None. The only prerequisites are:

- Python 3.12
- The packages listed in `pyproject.toml` (`pytest`, `black`, `isort`, `ruff`, `pre-commit`)
- Pre-commit hooks installed via `pre-commit install`

No database, no message broker, no external network access required.
