def find_by_name(node, text):
    if node.spelling == text:
        return node
    for n in node.get_children():
        r = find_by_name(n, text)
        if r is not None:
            return r
    return None


def stub_lexicon(value):
    from devana.syntax_abstraction.organizers.lexicon import Lexicon
    value.lexicon = Lexicon()
