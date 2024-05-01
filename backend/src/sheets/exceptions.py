
class SheetAPIException(Exception):
    pass


class SheetCreationException(SheetAPIException):
    pass


class InvalidSheetSchemaException(SheetCreationException):
    pass
