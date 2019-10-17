from typing import Optional, List, Dict, Any
from pyAitu.utils.dictionary_extractor import dictionary_of_object_if_exist

# Type aliases
Object = Any
Array = List
Objects = Array[Object]
Dictionaries = Array[Dict[Any, Any]]


def serialized(objects: Optional[Objects]) -> Optional[Dictionaries]:
    if not isinstance(objects, Array) or objects is None:
        return None
    objects = list(map(lambda object: dictionary_of_object_if_exist(object), objects))
    objects = list(filter(None, objects))
    return objects
