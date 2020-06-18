from typing import Dict, List, Union


class BaseError(Exception):
    messages: Union[str, List, Dict] = None


class SaveError(BaseError):
    pass


class DeleteError(BaseError):
    pass


class ValidationError(BaseError):
    pass
