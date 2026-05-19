from app.core.data_loader import clear_data_caches


def clear_backend_caches() -> None:
    clear_data_caches()

    # Import lazily to avoid circular imports at module load time.
    from app.core.analytics_engine import clear_analytics_engine_cache

    clear_analytics_engine_cache()
