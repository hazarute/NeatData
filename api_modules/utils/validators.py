"""
Input Validators
================
İstek doğrulama fonksiyonları.
"""

from typing import List


def validate_operation(operation: str) -> bool:
    """
    Belirtilen işlem geçerliliğini kontrol et.
    
    Args:
        operation: Kontrol edilecek işlem adı
    
    Returns:
        bool: Geçerliyse True, değilse False
    """
    valid_operations = {"trim", "lowercase", "uppercase"}
    return operation in valid_operations


def validate_operations(operations: List[str]) -> bool:
    """
    İşlem listesinin geçerliliğini kontrol et.
    
    Args:
        operations: Kontrol edilecek işlem listesi
    
    Returns:
        bool: Tüm işlemler geçerliyse True
    """
    if not operations:
        return False
    
    return all(validate_operation(op) for op in operations)
