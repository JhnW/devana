from typing import List, Union, Optional
from devana.syntax_abstraction.organizers.lexicon import Lexicon


def namespaces_string(source: Optional[Union[List[str], List[Lexicon]]]) -> str:
    if source is None:
        return ""
    namespaces = []
    for s in source:
        if isinstance(s, str):
            namespaces.append(s)
        elif isinstance(s, Lexicon):
            namespaces.append(s.namespace)
        else:
            raise ValueError("Not know type.")
    return "::".join(namespaces)
