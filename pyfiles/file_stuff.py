from __future__ import annotations

from pathlib import Path

import pandas as pd


def ensure_folder(path_obj: Path) -> Path:
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def save_csv(df: pd.DataFrame, out_path: Path) -> None:
    df.to_csv(out_path, index=False)
