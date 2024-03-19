from typing import Callable

# *** This factory is necessery mainly to avoid
# *** "existing endpoint function" error with flask routers


def decorator_factory(
        decorator_name_modifier,
        decorator: Callable[[Callable], Callable]
) -> Callable[[Callable], any]:
    def modified_decorator(*args, **kwargs):
        decorated_function = decorator(*args, **kwargs)
        decorated_function.__name__ = f"{decorator_name_modifier}_{id(decorated_function)}"
        return decorated_function
    return modified_decorator
