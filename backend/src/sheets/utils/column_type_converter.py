from distutils.util import strtobool


COLUMN_TYPE_VALUE_CONVERTER = {
    "boolean": strtobool,
    "int": int,
    "double": float,
    "string": str
}
