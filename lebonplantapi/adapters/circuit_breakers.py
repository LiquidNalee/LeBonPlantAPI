import logging
from functools import wraps
from typing import Any, Callable, List, Type

from pycircuitbreaker import CircuitBreaker, CircuitBreakerRegistry


logger = logging.getLogger(__name__)


def _on_open(circuit: CircuitBreaker, exc: Exception) -> None:
    logger.warning(f"Circuit breaker {circuit.id} opened because of {exc}")


def _on_close(circuit: CircuitBreaker) -> None:
    logger.info(f"Circuit breaker {circuit.id} closed")


def init_breaker(
    registry: CircuitBreakerRegistry,
    breaker_id: str,
    exception_denylist: List[Type[Exception]],
    error_threshold: int = 5,
    recovery_timeout: int = 30,
    recovery_threshold: int = 1,
) -> Callable:
    circuit = CircuitBreaker(
        breaker_id=breaker_id,
        error_threshold=error_threshold,
        recovery_timeout=recovery_timeout,
        recovery_threshold=recovery_threshold,
        # FIXME: pycircircuitbreaker typing broken
        exception_denylist=exception_denylist,  # type: ignore
        on_open=_on_open,
        on_close=_on_close,
    )

    registry.register(circuit)

    def breaker(func: Callable) -> Callable:
        @wraps(func)
        def circuit_wrapper(*args: Any, **kwargs: Any) -> Any:
            return circuit.call(func, *args, **kwargs)

        return circuit_wrapper

    return breaker


circuit_breaker_registry = CircuitBreakerRegistry()
