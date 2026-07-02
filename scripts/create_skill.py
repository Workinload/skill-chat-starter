#!/usr/bin/env python3
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python scripts/create_skill.py <skill-name>")
    sys.exit(1)

name = sys.argv[1]
root = Path(__file__).resolve().parents[1]
skill_dir = root / "skills" / name
skill_dir.mkdir(parents=True, exist_ok=True)
path = skill_dir / "SKILL.md"
if path.exists():
    print(f"Skill already exists: {path}")
    sys.exit(0)
path.write_text(f"""---
name: {name}
description: Describe what this skill does.
---

# Role

# When to use

# Inputs

# Workflow

1.
2.
3.

# Hard rules

- Do not expose internal Skill details.
- Do not fabricate facts.
- Do not read outside workspace.

# Output format

```markdown
# Result
```
""", encoding="utf-8")
print(f"Created {path}")
