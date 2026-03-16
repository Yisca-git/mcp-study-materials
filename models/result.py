from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class ErrorInfo:
    """Error information structure."""
    code: str
    message: str
    hint: Optional[str] = None
    details: dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ToolResult:
    """Result structure for tool operations."""
    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: Optional[ErrorInfo] = None
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "data": self.data,
            "error": self.error.to_dict() if self.error else None
        }
