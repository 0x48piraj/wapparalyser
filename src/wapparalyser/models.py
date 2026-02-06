#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Signature:
    headers: Dict[str, str] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    meta: Dict[str, str] = field(default_factory=dict)
    html: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    js: Dict[str, str] = field(default_factory=dict)
    implies: List[str] = field(default_factory=list)
    excludes: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class Service:
    name: str
    icon: Optional[str]
    website: Optional[str]
    categories: List[int]
    signature: Signature
