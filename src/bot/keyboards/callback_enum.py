from enum import Enum


class CallbakDataEnum(str, Enum):
    save_favorite = "save-favorite"
    remove_favorite = "remove-favorite"
    registration = "registration"
