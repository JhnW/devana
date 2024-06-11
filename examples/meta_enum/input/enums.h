#ifndef ENUMS_HPP
#define ENUMS_HPP

enum class AnimalPetKind
{
    DOG,
    CAT,
    HAMSTER,
    PARROT,
    GOLDEN_FISH
};

enum class AnimalPetState
{
    OK = 0x0,
    HUNGRY = 0x2,
    SICK = 0x4,
    ANGRY = 0x6
};

#endif