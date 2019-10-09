from typing import Dict, List, Optional


def extract_property_if_exist_from(object: any, property_name: str) -> Optional[any]:
    if hasattr(object, "__getattribute__") and hasattr(object, property_name):
        return object.__getattribute__(property_name)
    else:
        return None


def extract_dictionary_if_exist_from(object: any) -> Optional[Dict[str, any]]:
    dictionary = extract_property_if_exist_from(object, property_name="__dict__")
    return None if not dictionary else dictionary
