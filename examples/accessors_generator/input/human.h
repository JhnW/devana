#ifndef HUMAN_H
#define HUMAN_H

#include <iostream>
#include <string>

class Human {
private:
    // devana: ignore-attributes
    std::string name;

    std::string lastName;

    // devana: custom-name=Age
    int _age;

    // devana: ignore-field
    double height;

    double weight;
public:
    Human(const std::string &name, const std::string &lastName, int age, double height, double weight):
        name(name), lastName(lastName), _age(age), height(height), weight(weight) {}

    [[maybe_unused]]
    void say() const {
        std::cout << "Hello! My name is " << getName() << std::endl;  // The getName method will be generated.
    }
};

#endif //HUMAN_H