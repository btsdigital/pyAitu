from typing import Optional, Union, List, Dict, Any
from pyAitu.utils.dictionary_extractor import dictionary_purified_from_none, dictionary_of_object_if_exist
from .options import Options
from .header import Header
from .bottom_bar import BottomBar
import logging

# Type aliases
Void = None
Array = List
Object = Any
String = str
Dictionaries = List[Dict[String, Object]]
ArrayOrObject = Union[Array[Object], Object]


# Function with side effect on input dictionaries
def add_purified_object_dictionary_if_possible_to(dictionaries: Dictionaries, obj: Object) -> Void:
    object_dictionary = dictionary_of_object_if_exist(obj)
    if object_dictionary is not None:
        dictionaries.append(dictionary_purified_from_none(object_dictionary))


def make_dictionaries_from(array_or_object: ArrayOrObject) -> Dictionaries:
    dictionaries: Dictionaries = []
    if isinstance(array_or_object, Array):
        array = array_or_object
        for obj in array:
            add_purified_object_dictionary_if_possible_to(dictionaries, obj)
    else:
        obj = array_or_object
        add_purified_object_dictionary_if_possible_to(dictionaries, obj)
    return dictionaries


class Form:
    def __init__(
            self,
            _id: String,
            content: ArrayOrObject,
            header: Header,
            options: Optional[Options] = None,
            bottom_bar: Optional[BottomBar] = None
    ):
        self.id = _id
        self.header = header
        self.content = content
        self.options = options
        self.bottom_bar = bottom_bar

    def make_dictionary(self) -> Dict[String, Any]:
        dictionary = {
            "id": self.id,
            "content": make_dictionaries_from(self.content)
        }
        header_dictionary = dictionary_of_object_if_exist(self.header)
        if header_dictionary:
            dictionary["header"] = header_dictionary
        else:
            logger = logging.getLogger('Form(make_dictionary)')
            logger.error('Can not get Dictionary of Header! Header is required attribute')
            return None

        if self.options:
            dictionary["options"] = dictionary_of_object_if_exist(self.options)

        if self.bottom_bar:
            dictionary["bottom_bar"] = dictionary_of_object_if_exist(self.bottom_bar)
        return { "form": dictionary }
