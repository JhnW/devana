from dataclasses import dataclass


@dataclass
class Configuration:
    """Parser core configuration."""
    orphaned_enum_values_allowed: bool = False
    """An orphaned enum is an enum value not preceded by an enum name. For example, EnumTypeName.Value1 is the standard
    value notation, but the user can only use Value1 in a given context - a parser based on the expected argument type
    can match the argument type.
    This option is mainly useful for simple preprocessors that do not use unions."""
    property_overload_allowed: bool = False
    """Allows multiple properties with the same name (within namespace) with different argument types.
    Does not affect the ability to use default arguments."""
    ignore_unknown: bool = False
    """An option that determines whether to ignore a syntactically valid property with an unknown name without error.
    This does not apply to cases where unknown values assigned to a property with a known name.
    This option can be partially ignored for special parsers. In particular, C++11 attribute-based parsers may partially
    ignore this setting in order to more easily implement compiler extension attributes - this applies to the global
    namespace, so it is recommended for such parsers to always use their own namespaces."""
