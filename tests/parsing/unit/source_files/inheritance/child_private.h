/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef CHILD_PRIVATE_H__
#define CHILD_PRIVATE_H__

#include "parents.h"

class Child : private Parent1, Parent2
{
    Child();

public:
    int val;
};
#endif
