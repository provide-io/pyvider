from pyvider.functions.decorators import register_function


@register_function("discovered_sample_function", summary="A discovered function.")
def discovered_sample_function(a: int, b: int) -> int:
    return a + b
