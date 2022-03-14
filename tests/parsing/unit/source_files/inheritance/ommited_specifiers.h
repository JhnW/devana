/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef INHERITANCE_CHILD_H__
#define INHERITANCE_CHILD_H__

class BaseClass
{
public:
    void genericMethod(int genericInt);

private:
    int _genericVal;
};

struct BaseStruct
{
    void doSomething();

private:
    int _val;
};

class DerivedClass : BaseClass, BaseStruct
{
};
#endif
