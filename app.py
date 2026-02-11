"""
Entry point for Streamlit Cloud.

This small wrapper avoids the space in the folder name ("Assessment 1"),
which was confusing the Streamlit dependency installer and causing
errors like `1/requirements.txt`.

Cloud main file path: `app.py`
"""

import os
import sys
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    app_dir = base_dir / "Assessment 1"

    # Ensure the inner app can be imported and its relative paths work
    sys.path.insert(0, str(app_dir))
    os.chdir(app_dir)

    import rag_streamlit_app  # type: ignore

    rag_streamlit_app.main()


if __name__ == "__main__":
    main()

