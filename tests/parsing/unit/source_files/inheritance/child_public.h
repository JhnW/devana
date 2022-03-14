/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef CHILD_PUBLIC_H__
#define CHILD_PUBLIC_H__

#include "parents.h"

class Child : public Parent1, Parent2
{
    Child();

public:
    int val;
};

#endif
