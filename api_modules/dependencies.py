"""
Dependency Injection
====================
FastAPI Depends() kullanılan bağımlılıklar.
"""

from modules.pipeline_manager import PipelineManager


def get_pipeline_manager() -> PipelineManager:
    """
    PipelineManager factory fonksiyonu.
    
    FastAPI dependency injection kullanarak her istek için
    yeni bir PipelineManager örneği sağlar.
    
    Returns:
        PipelineManager: Yeni PipelineManager örneği
    """
    return PipelineManager()
