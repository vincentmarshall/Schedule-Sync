from datetime import datetime
from cal_setup import get_calendar_service


def main(day, month, year, shiftStartHr, shiftStartMn, shiftEndHr, shiftEndMn, position):
   service = get_calendar_service()

   startTime = datetime(int(year), int(month), int(day), int(shiftStartHr), int(shiftStartMn))
   start = startTime.isoformat()
   endTime = datetime(int(year), int(month), int(day), int(shiftEndHr), int(shiftEndMn))
   end = endTime.isoformat()

   event_result = service.events().insert(calendarId='6c1obre6q5h2t66vc3l4aji3u8@group.calendar.google.com',
       body={
           "summary": position,
           "description": 'Your shift at Cineplex Yonge and Dundas',
           "start": {"dateTime": start, "timeZone": 'Canada/Eastern'},
           "end": {"dateTime": end, "timeZone": 'Canada/Eastern'},
           "colorId": "3"
       }
   ).execute()

   print("created event")
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
   main()