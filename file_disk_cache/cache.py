from __future__ import annotations

from diskcache import Cache, ENOVAL

from file_disk_cache.file_disk import FileDisk


def call_with_cache(
    func: Callable,
    path: str,
    cache: Cache,
    args: list[Any] = None,
    kwargs: dict[str, Any] = None,
    **cache_kwargs,
) -> Any:
    """A light wrapper around a function that saves the output to the cache.

    The key provided is used as the key to save the cache.
    """

    if args is None:
        args = []

    if kwargs is None:
        kwargs = {}

    if not isinstance(cache.disk, FileDisk):
        raise ValueError(
            f"This function is only intended to be called with caches that use a FileDisk. This cache uses: {type(cache.disk)}. "
            "Most likely you can use the cache.memoize is more suitable than call_with_cache."
        )

    result = cache.get(path, default=ENOVAL, retry=True)

    if result is ENOVAL:
        result = func(*args, **kwargs)
        expire = cache_kwargs.get("expire", None)
        tag = cache_kwargs.get("tag", None)

        if expire is None or expire > 0:
            cache.set(path, result, expire, tag=tag, retry=True)

    return result
