/**
 *   SPDX-FileCopyrightText: Copyright (C) <2022> Critical TechWorks, SA
 * 
 *   SPDX-License-Identifier: LGPL-2.1-only
 */

#ifndef COMMENTS_H__
#define COMMENTS_H__

namespace example
{
/**
 *  This is the documentation for the Example.
 **/
class Example
{
    Example();

    /** Returns 42 */
    int doSomething() { return 42; }

public:
    int val;
};
} // namespace example
#endif
