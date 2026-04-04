"""Allow ``python -m whispernote`` (delegates to cli.main)."""
from .cli import main

if __name__ == "__main__":
    main()
