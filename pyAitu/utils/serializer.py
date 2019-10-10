from typing import Optional, List, Dict
from pyAitu.utils.dictionary_extractor import extract_dictionary_if_exist_from


def serialized(objects: Optional[list]) -> Optional[List[Dict[str, any]]]:
    if not isinstance(objects, list) or not objects:
        return None
    objects = list(map(lambda object: extract_dictionary_if_exist_from(object), objects))
    objects = list(filter(None, objects))
    return objects
