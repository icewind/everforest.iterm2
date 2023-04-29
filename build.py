#!/usr/bin/env python

from typing import Tuple, Dict, Union
import json
import plistlib
import operator
from functools import reduce
from pathlib import Path

NAME = "everforest"
VARIANTS = ["light", "dark"]
CONTRASTS = ["hard", "medium", "low"]
OUT_DIR = "themes"
THEME_FILE = "theme.json"
PALETTE_FILE = "palette.json"


def get_color_components(hex: str) -> Tuple[float, float, float]:
    return tuple(int(hex[i + 1 : i + 3], 16) / 255 for i in (0, 2, 4))


def get_color_dict(
    components: Tuple[float, float, float]
) -> Dict[str, Union[str, float]]:
    return {
        "Color Space": "sRGB",
        "Red Component": components[0],
        "Green Component": components[1],
        "Blue Component": components[2],
        "Alpha Component": 1.0,
    }


if __name__ == "__main__":
    with open(THEME_FILE) as f:
        theme = json.load(f)
    with open(PALETTE_FILE) as f:
        palette = json.load(f)

    out_dir = Path(OUT_DIR)
    out_dir.mkdir(exist_ok=True)

    for variant in VARIANTS:
        for contrast in CONTRASTS:
            file_name = f"{NAME}_{variant}_{contrast}.itermcolors"
            file_path = out_dir / file_name
            content = theme.copy()

            for name, slug in content.items():
                if "." in slug:
                    path = slug
                else:
                    path = f"{variant}.{'background.' + contrast if slug.startswith('bg') else 'foreground'}.{slug}"
                content[name] = get_color_dict(
                    get_color_components(
                        reduce(operator.getitem, path.split("."), palette)
                    )
                )

            with open(file_path, "wb") as f:
                plistlib.dump(content, f)
