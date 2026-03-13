import os
import json
import hashlib
from typing import Dict, List

CACHE_PATH = "classifier_cache.json"

if os.path.exists(CACHE_PATH):
    try:
        with open(CACHE_PATH, "r") as f:
            _CACHE = json.load(f)
    except Exception:
        _CACHE = {}
else:
    _CACHE = {}


def _save_cache():
    try:
        with open(CACHE_PATH, "w") as f:
            json.dump(_CACHE, f)
    except Exception:
        pass


def _local_heuristic(prompt: str) -> (str, float):
    p = prompt.lower()
    if "summariz" in p or "tl;dr" in p:
        return "summarization", 0.9
    if "extract" in p or "entities" in p or "parse" in p:
        return "extraction", 0.88
    if "classif" in p or "sentiment" in p or "label" in p:
        return "classification", 0.88
    if "write a function" in p or "implement" in p or "code" in p:
        return "coding", 0.9
    if "why" in p or "reason" in p or "explain" in p:
        return "reasoning", 0.7
    if "hello" in p or "hi" in p or "chat" in p:
        return "conversation", 0.8
    return "other", 0.6


def classify_task(prompt: str) -> Dict:
    key = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if key in _CACHE:
        return _CACHE[key]

    task_type, conf = _local_heuristic(prompt)
    result = {"task_type": task_type, "confidence": conf}
    _CACHE[key] = result
    _save_cache()
    return result


def classify_batch(prompts: List[str]) -> List[Dict]:
    return [classify_task(p) for p in prompts]
