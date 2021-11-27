from typing import Any, Callable

from .settings import session


def db_accessor(commit: bool = False) -> Callable:
    def repo_method_decorator(repo_method: Callable) -> Callable:
        async def repo_method_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await repo_method(*args, **kwargs)
                if commit:
                    await session.commit()
                return result
            except Exception:
                if commit:
                    await session.rollback()
                raise
            finally:
                await session.close()

        return repo_method_wrapper

    return repo_method_decorator
