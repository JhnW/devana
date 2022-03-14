/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef HEADER_GUARD_H
#define HEADER_GUARD_H

struct Test1
{
    int a;
};

struct Test2
{
    double a;
    float* c;
};

Test2* foo();

#endif /** HEADER_GUARD_H **/
