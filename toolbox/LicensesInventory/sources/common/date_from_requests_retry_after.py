#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Software Name: floss-toolbox
# SPDX-FileCopyrightText: Copyright (c) Orange SA
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache 2.0 license,
# the text of which is available at https://opensource.org/license/apache-2-0
# or see the "LICENSE.txt" file for more details.
#
# Authors: See CONTRIBUTORS.txt
# Software description: A toolbox of scripts to help work of forges admins and open source referents

from datetime import date, time, datetime, timedelta

class CDateFromRetryAfter:

    def manage_delay_in_seconds(self, my_date):
        result = None

        try:
            seconds = int(my_date)
            current_date_time = datetime.utcnow()
            result = current_date_time + timedelta(seconds=seconds)
        except Exception as e:
            result = None

        return result

    def manage_delay_in_date(self, my_date):
        result = None

        # convert date from requests to datetime
        try:
            format_http = "%a, %d %b %Y %H:%M:%S GMT"
            result = datetime.strptime(my_date, format_http)
        except Exception as e:
            result = None

        return result

    def get_the_months(self):
        the_months = {
            'january': '01',
            'february': '02',
            'march': '03',
            'april': '04',
            'may': '05',
            'june': '06',
            'july': '07',
            'august': '08',
            'september': '09',
            'october': '10',
            'november': '11',
            'december': '12'
        }

        return the_months

    def search_year_with_4_numbers(self, my_date, the_numbers):
        year_before = True

        number = 0
        i = -1
        for i in range(0, len(my_date)):
            c = my_date[i]

            if c in the_numbers:
                number += 1
                continue

            if number == 2:
                year_before = False

            if number == 4:
                break

            number = 0

        if number == 4:
            if i == (len(my_date) -1):
                i += 1
            i_year = i -4
        year = my_date[i_year:i_year +4]

        i_separator = i +0
        if year_before == False:
            i_separator = i_year -1

        return (year, i_separator, year_before)

    def get_month(self, my_date, year_before, i_separator):
        month = str()
        month_with_letters = str()

        the_months = self.get_the_months()
        for my_month, my_number in the_months.items():
            if my_month in my_date.lower():
                month = my_number
                month_with_letters = my_month
                break
            my_month_with_3_letters = my_month[0:3]
            if my_month_with_3_letters in my_date.lower():
                month = my_number
                month_with_letters = my_month_with_3_letters
                break

        if month == str():
            if year_before == True:
                i_month = i_separator +1
            else:
                i_month = i_separator -2
            month = my_date[i_month:i_month +2]

        return (month, month_with_letters)

    def get_day(self, my_date, year_before, i_separator, month_with_letters):
        day = str()

        i_day = 999
        if month_with_letters == str():
            s_month = 2
        else:
            s_month = len(month_with_letters)

        if year_before == True:
            i_separator = i_separator + s_month + 1
            i_day = i_separator +1
        else:
            i_separator = i_separator - s_month -1
            i_day = i_separator -2
        day = my_date[i_day:i_day +2]

        return day

    def convert_seconds_to_hours_minutes_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        #return "%d h %02d min %02d sec" % (hours, minutes, seconds)
        return (hours, minutes, seconds)

    def manage_delay_from_today(self, next_date_time_utc):
        next_date_time_utc = next_date_time_utc + timedelta(minutes=1)

        # delay from current date time
        current_date_time_utc = datetime.utcnow()
        result = next_date_time_utc - current_date_time_utc

        return result

    def get(self, my_date):
        # to manage the date at format:
        # Wed, 14 Feb 2024 18:00:00 GMT
        # or in seconds

        next_date = self.manage_delay_in_seconds(my_date)
        if next_date == None:
            next_date = self.manage_delay_in_date(my_date)
        if next_date == None:
            return None

        delay = self.manage_delay_from_today(next_date)

        next_date = next_date.strftime('%Y-%m-%d %H:%M:%S')

        delay = str(delay)
        # remove the micro-seconds
        p = delay.find('.')
        delay = delay[0:p]

        return (next_date, delay)
