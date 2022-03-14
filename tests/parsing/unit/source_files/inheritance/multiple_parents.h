/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef INHERITANCE_CHILD_H__
#define INHERITANCE_CHILD_H__

#include "parents.h"

class BaseClass
{
};

class DerivedClass : public Parent1, private Parent2, protected BaseClass
{
};
#endif
