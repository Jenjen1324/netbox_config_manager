
def _setup_model_helpers():
    """
    Puts the serializers into this namespace
    """
    g = globals()
    from ..simple_models import MODEL_REGISTRY
    for model in MODEL_REGISTRY:
        serializer = model.api_serializer
        g[serializer.__name__] = serializer

_setup_model_helpers()
