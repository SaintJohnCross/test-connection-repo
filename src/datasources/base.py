# defines datasource contraxts and allows quick swap on implementations
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Any, Dict, List, Optional, Literal

StatementKey = Literal[
    "income_statement",
    "balance_sheet",
    "cash_flow",
    "ratios_ttm",
    "key_metrics_ttm",
]

@dataclass(frozen=True)
class statementRequest:
    symbol: str
    statement_type: StatementKey
    limit: int = 1
    period: Literal["annual", "quarter"] = "quarter"


class DataSourceError(RuntimeError):
    """Raised when a datasource operation fails."""

class DataSourceAuthError(DataSourceError):
    """Raised when a datasource authentication fails."""

class DataSourceNotFoundError(DataSourceError):
    """Raised when a datasource is not found."""

class DataSourceRateLimitError(DataSourceError):
    """Raised when a datasource rate limit is exceeded."""

class FinancialDataSource(Protocol):
    """
    A provider that can return financial statement-like data in a consistent format.
    Implementations: FMPDataSource, FixtureDataSource, later DBDataSource, etc.
    """

    name: str

    def get_statement(self, request: statementRequest) -> List[Dict[str, Any]]:
        """Return a list of records (dicts), matching the provider's statement schema."""