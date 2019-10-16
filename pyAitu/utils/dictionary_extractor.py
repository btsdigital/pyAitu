from typing import Dict, Optional, Any
import copy

# Type aliases
Object = Any
String = str


def property_of_object_if_exist(object: Optional[Object], property_name: String) -> Optional[Any]:
    if object is None:
        return None
    if hasattr(object, "__getattribute__") and hasattr(object, property_name):
        return object.__getattribute__(property_name)
    else:
        return None


def dictionary_of_object_if_exist(object: Optional[Object]) -> Optional[Dict[Any, Any]]:
    return property_of_object_if_exist(object, property_name="__dict__")


# Shallow purification from None on arbitrary Python Dictionaries. Returns purified dictionary.
def dictionary_purified_from_none(dictionary: Dict[Any, Any]) -> Dict[Any, Any]:
    return dict(filter(lambda item: item[1], dictionary.items()))


# Shallow purification from None on arbitrary Python Objects. Returns purified deepcopy of object.
def object_purified_from_none(object: Object) -> Object:
    new_object = copy.deepcopy(object)
    object_dictionary = dictionary_of_object_if_exist(new_object)
    if object_dictionary is not None:
        new_object.__dict__ = dictionary_purified_from_none(object_dictionary)
    return new_object
