from redis_proxy import configure_redis_proxy


def start(redis_address, cache_exp_secs, cache_max_keys):
    proxy = configure_redis_proxy(redis_address, float(cache_exp_secs),
                                  int(cache_max_keys))
    return proxy
