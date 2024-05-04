class SheetAPIException(Exception):
    pass


class InvalidCellTypeException(SheetAPIException):
    pass


class InvalidCellValueException(SheetAPIException):
    pass


class SheetCreationException(SheetAPIException):
    pass


class InvalidSheetSchemaException(SheetCreationException):
    pass


class DatabaseObjectNotFoundException(SheetAPIException):
    pass
