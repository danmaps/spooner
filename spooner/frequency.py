"""
Utilities for ranking spoonerism candidates using word frequency data.
"""

from __future__ import annotations

import json
import math
import re
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

BASELINE_SCORE = 1.5
APOSTROPHE_PENALTY = 0.4
ALPHA_ONLY_PENALTY = 0.6
FREQ_PATH = Path(__file__).resolve().parent.parent / "static" / "freq.json"
NON_ALPHA_EDGES = re.compile(r"^[^a-z]+|[^a-z]+$")


@lru_cache(maxsize=1)
def _load_frequency_map() -> Dict[str, float]:
    """
    Load the JSON frequency file and convert counts into log-scale scores.
    """
    with FREQ_PATH.open(encoding="utf-8") as handle:
        raw_entries = json.load(handle)

    freq_map: Dict[str, float] = {}
    for entry in raw_entries:
        word = (entry.get("word") or "").strip().lower()
        count = max(int(entry.get("count") or 0), 1)
        if not word:
            continue
        freq_map[word] = math.log10(count)
    return freq_map


def _strip_edges(token: str) -> str:
    """
    Remove leading/trailing punctuation and digits from a token.
    """
    return NON_ALPHA_EDGES.sub("", token.lower())


def score_word(raw_word: str) -> float:
    """
    Return a Zipf-like score for a word, penalizing fallback matches.
    """
    if not raw_word:
        return BASELINE_SCORE

    freq_map = _load_frequency_map()
    normalized = _strip_edges(raw_word)
    candidates: List[Tuple[str, float]] = []
    if normalized:
        candidates.append((normalized, 0.0))

    no_apostrophe = normalized.replace("'", "")
    if no_apostrophe and no_apostrophe != normalized:
        candidates.append((no_apostrophe, APOSTROPHE_PENALTY))

    alpha_only = re.sub(r"[^a-z]", "", normalized)
    if alpha_only and alpha_only not in {normalized, no_apostrophe}:
        candidates.append((alpha_only, ALPHA_ONLY_PENALTY))

    for candidate, penalty in candidates:
        if candidate in freq_map:
            return max(freq_map[candidate] - penalty, BASELINE_SCORE)

    return BASELINE_SCORE


def _dedupe_preserve_order(items: Sequence[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for item in items:
        if item in seen:
            continue
        ordered.append(item)
        seen.add(item)
    return ordered


def sort_candidates_by_frequency(candidates: Iterable[str]) -> List[str]:
    """
    Sort a set of candidate spellings by descending frequency.
    """
    deduped = _dedupe_preserve_order(list(candidates))
    return sorted(deduped, key=score_word, reverse=True)


def rank_candidate_pairs(
    first_candidates: Sequence[str], second_candidates: Sequence[str]
) -> List[Dict[str, object]]:
    """
    Generate a sorted list of candidate word pairs using the min/avg heuristic.
    """
    pairs = []
    for first_word, second_word in product(first_candidates, second_candidates):
        first_score = score_word(first_word)
        second_score = score_word(second_word)
        primary = min(first_score, second_score)
        secondary = (first_score + second_score) / 2
        pairs.append(
            {
                "words": [first_word, second_word],
                "scores": [first_score, second_score],
                "primary": primary,
                "secondary": secondary,
            }
        )

    pairs.sort(key=lambda entry: (entry["primary"], entry["secondary"]), reverse=True)
    return pairs
