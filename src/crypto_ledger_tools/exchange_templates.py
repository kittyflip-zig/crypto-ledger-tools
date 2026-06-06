from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


KNOWN_COMPANY_PREFIXES = ("SBIVC", "GMO", "BitFlyer", "BitPoint")
PLACEHOLDER_PATTERNS = ("YYYYMMDD", "YYYYMM", "YYYY")
DYNAMIC_COLUMN_PREFIXES = ("残高_",)


@dataclass(frozen=True)
class TemplateInspection:
    template_name: str
    normalized_report_name: str
    dynamic_columns: tuple[str, ...]


def normalize_report_filename(path: str | Path) -> str:
    """Normalize template and actual CSV names for loose report matching."""
    name = Path(path).stem
    for prefix in KNOWN_COMPANY_PREFIXES:
        if name.lower().startswith(prefix.lower() + "_"):
            name = name[len(prefix) + 1 :]
            break
    for placeholder in PLACEHOLDER_PATTERNS:
        name = name.replace(placeholder, "")
    name = re.sub(r"\d{4,8}", "", name)
    name = re.sub(r"[-_]+", "_", name).strip("_")
    return name.lower()


def detect_dynamic_asset_columns(headers: list[str]) -> list[str]:
    dynamic: list[str] = []
    for header in headers:
        clean = header.strip()
        if any(clean.startswith(prefix) for prefix in DYNAMIC_COLUMN_PREFIXES):
            dynamic.append(clean)
    return dynamic


def adjusted_headers_for_actual_csv(
    template_headers: list[str],
    actual_headers: list[str],
) -> list[str]:
    """Return headers that keep template order but use actual dynamic asset columns."""
    template_dynamic = set(detect_dynamic_asset_columns(template_headers))
    actual_dynamic = detect_dynamic_asset_columns(actual_headers)

    adjusted: list[str] = []
    inserted_dynamic = False
    for header in template_headers:
        clean = header.strip()
        if clean in template_dynamic:
            if not inserted_dynamic:
                adjusted.extend(actual_dynamic)
                inserted_dynamic = True
            continue
        adjusted.append(clean)

    if not inserted_dynamic:
        adjusted.extend(actual_dynamic)

    for header in actual_headers:
        clean = header.strip()
        if clean and clean not in adjusted:
            adjusted.append(clean)
    return adjusted


def inspect_template(path: str | Path, headers: list[str]) -> TemplateInspection:
    return TemplateInspection(
        template_name=Path(path).name,
        normalized_report_name=normalize_report_filename(path),
        dynamic_columns=tuple(detect_dynamic_asset_columns(headers)),
    )
