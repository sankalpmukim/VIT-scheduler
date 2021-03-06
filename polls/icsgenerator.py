from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json
import os
# fp = open('vitfullpagetimetable.txt', newline='')
# print(repr(fp.read()))
# fp.seek(0,0)
# allTheFriggingLines = fp.readlines()
# startIndex = allTheFriggingLines.index('1\r\n')
# endIndex = -19
# length = len(allTheFriggingLines)


# def connectThese(lst):
#     strng = []
#     for i in lst:
#         strng.append(i[:-2])
#     return strng


# relevantData = [connectThese(allTheFriggingLines[i:i+31])
#                 for i in range(startIndex, length-endIndex, 31)][:-2]
# # print(allTheFriggingLines)
# for i in relevantData:
#     print(i)

def get_relevant_data(strng: str):

    def connect_these(lst):
        strnges = []
        for i in lst:
            strnges.append(i)
        return strnges
    allTheFriggingLines = strng.split('\\r\\n')
    startIndex = allTheFriggingLines.index('1')
    print(startIndex)
    endIndex = -19
    length = len(allTheFriggingLines)
    relevantData = [connect_these(allTheFriggingLines[i:i+31])
                    for i in range(startIndex, length-endIndex, 31)][:-2]
    # for i in relevantData:
    #     print(i)
    return relevantData[:], allTheFriggingLines[2][11:20]


def build_event_duration(summary, description, start, duration, location,
                         freq_of_recurrence, until):
    '''
    Return an event that can be added to a calendar

    summary: summary of the event
    description: description of the event
    location: self explanatory
    start, end, stamp: These are datetime.datetime objects
    freq_of_recurrence: frequency of recurrence, string which can take the
    values daily, weekly, monthly, etc.
    until: A datetime.datetime object which signifies when the recurrence will
    end
    '''

    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', start)
    event.add('duration', duration)
    event.add('dtstamp', datetime.now())
    event.add('location', location)
    event.add('rrule', {'FREQ': freq_of_recurrence, 'UNTIL': until})

    return event


# cal.add_component(build_event_duration('this is summary', 'this is description', datetime(
#     2021, 2, 22, 8, 0, 0), 1, 'location', 'daily', datetime(2021, 7, 1, 0, 0, 0)))

#
def generate_calendar(whole_site_data: str):
    cal = Calendar()
    cal.add('profid', 'abcd')
    cal.add('version', '4.0.7')
    cal.add('x-wr-timezone', 'Asia/Kolkata')
    cal.add('x-wr-calname', 'testCalendar')
    slotfile = open('./polls/slotinfofile.json', 'r')
    slotinfo = json.load(slotfile)
    relevantData, reg_no = get_relevant_data(whole_site_data)
    print(reg_no)
    for course in relevantData:
        summary = course[4].split('-')[0][:-1]+course[6]
        description = course[4].split('-')[1][1:]
        slots = course[15][:-2].split('+')
        year = 2021
        month = 2
        duration = timedelta(minutes=45)
        until = datetime(2021, 6, 19)
        location = course[-13]+'('+course[20][:-2]+')'
        for slot in slots:
            for clas in slotinfo[slot]:
                event = build_event_duration(summary, description, datetime(
                    year, month, clas[1], clas[0][0], clas[0][1]), duration, location, freq_of_recurrence='weekly', until=until)
                cal.add_component(event)
    if os.path.exists(reg_no+'.ics'):
        os.remove(reg_no+'.ics')
    with open(reg_no+'.ics', 'wb') as ics:
        ics.write(cal.to_ical())
    print('calendar generation complete')
