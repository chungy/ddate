#!/usr/bin/env python

# Copyright (c) 2013 Mike Swanson <mikeonthecomputer@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


'''Converts between Discordian and Gregorian dates'''

import calendar
import datetime

DAYS = ('Sweetmorn', 'Boomtime', 'Pungenday',
        'Prickle-Prickle', 'Setting Orange')
DAYS_SHORT = ('SM', 'BT', 'PD', 'PP', 'SO')

SEASONS = ('Chaos', 'Discord', 'Confusion', 'Bureaucracy', 'The Aftermath')
SEASONS_SHORT = ('Chs', 'Dsc', 'Cfn', 'Bcy', 'Afm')

HOLIDAYS = {'Mungday': (0, 5), 'Chaoflux': (0, 50),
            'Mojoday': (1, 5), 'Discoflux': (1, 50),
            'Syaday': (2, 5), 'Confuflux': (2, 50),
            'Zaraday': (3, 5), 'Bureflux': (3, 50),
            'Maladay': (4, 5), 'Afflux': (4, 50)}

def to_gregorian(ddate):
    '''Converts a Discordian date to a Gregorian date

    Assumes the Discordian calendar is tied to the Gregorian one.
    That is, years divisible by 100 only observe St. Tib's Day if
    the year is also divisible by 400.

    Takes a dictionary like from_gregorian outputs.

    '''

    year = ddate['yold'] - 1166

    if ddate['sttibs'] is True:
        return datetime.date(year, 2, 29)

    day_of_year = SEASONS.index(ddate['season']) * 73 + ddate['day']
    date = datetime.datetime.strptime('{} {}'.format(year, day_of_year),
                                      '%Y %j')

    return datetime.date(year, date.month, date.day)

def from_gregorian(date):
    '''Converts a Gregorian date to a Discordian date

    Assumes the Discordian calendar is tied to the Gregorian one.
    That is, years divisible by 100 only observe St. Tib's Day if
    the year is also divisible by 400.

    '''

    is_leap_year = calendar.isleap(date.year)
    if date.month == 2 and date.day == 29:
        ddate = {
            'yold': date.year + 1166,
            'sttibs': True,
            }

        return ddate

    day_of_year = date.timetuple().tm_yday

    if is_leap_year and day_of_year >= 60:
        day_of_year -= 1 # Compensate for St. Tib's Day

    season, dday = divmod(day_of_year, 73)
    weekday = (season * 73 + dday) % 5 - 1

    ddate = {
        'yold': date.year + 1166,
        'sttibs': False,
        'season': SEASONS[season],
        'season_short': SEASONS_SHORT[season],
        'day': dday,
        'ordday': ordinal(dday),
        'weekday': DAYS[weekday],
        'weekday_short': DAYS_SHORT[weekday],
        }

    return ddate

def ordinal(number):
    ldig = number % 10
    l2dig = (number // 10) % 10
    if l2dig == 1:
        suffix = 'th'
    elif ldig == 1:
        suffix = 'st'
    elif ldig == 2:
        suffix = 'nd'
    elif ldig == 3:
        suffix = 'rd'
    else:
        suffix = 'th'

    return '{0}{1}'.format(number, suffix)

if __name__ == '__main__':
    ddate = from_gregorian(datetime.date.today())

    if ddate['sttibs'] is True:
        print("St. Tib's Day, YOLD {}".format(ddate['yold']))
    else:
        print("Today is {}, the {} day of {} in the YOLD {}".format(
            ddate['weekday'], ddate['ordday'], ddate['season'], ddate['yold']))
