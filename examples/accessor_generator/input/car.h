#ifndef CAR_H
#define CAR_H

#include <iostream>

class Car {
private:
    std::string brand;
    float speed;

    // Ignore maybe_unused and nodiscard attributes.
    // devana: ignore-attributes
    bool working;
public:
    [[maybe_unused]]
    void speedUp() {
        std::cout << "Speeeeed!" << std::endl;
        setSpeed(speed + 10.1);  // The setSpeed method will be generated.
    }
};

#endif //CAR_H