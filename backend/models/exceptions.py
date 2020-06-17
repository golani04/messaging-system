from typing import Dict, List, Union


class SaveError(Exception):
    messages: Union[str, List, Dict] = None


class DeleteError(Exception):
    messages: Union[str, List, Dict] = None


class ValidationError(Exception):
    messages: Union[str, List, Dict] = None
