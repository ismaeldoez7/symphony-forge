# Windows support

## Supported native path

Use Windows with Git for Windows (including Git Bash) and Python 3.10 or
newer. From Command Prompt or PowerShell, `forge.cmd` is the entry point. It
checks `py -3`, `python`, then `python3` for a supported interpreter before
handing off to Git Bash; when Git Bash is unavailable, it runs Forge with the
interpreter it found.

## Remediation

If no suitable Python is available, `forge.cmd` uses winget from its canonical
WindowsApps location to install Python in user scope, refreshes PATH from the
known per-user install location, and retries once. `forge init`, `forge adopt`,
and `forge upgrade` also run the fast hook check on Windows. When it is red,
they run the same user-scope prerequisite remediation and print a named
`doctor --fix` or manual-installer step if the check remains red.

Forge never launches an elevated process with `RunAs`. A package installer
may show its own Windows prompt. If winget or a prerequisite cannot complete
in user scope, install Git for Windows or Python from the URL printed in the
red row and rerun the command.

## WSL2 escape hatch

WSL2 is optional, not a prerequisite. Use it as an escape hatch when policy or
machine configuration prevents the supported native Windows path from
converging; inside WSL2, follow the normal Linux setup.
