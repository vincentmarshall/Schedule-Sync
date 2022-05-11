import datetime
from datetime import datetime
from cal_setup import get_calendar_service

def main():
   service = get_calendar_service()
   # Call the Calendar API

   now = datetime.now();
   startOfMonth = datetime(now.year,now.month,1).isoformat() + 'Z';

   #currentMonth = datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List of events')
   events_result = service.events().list(
       calendarId='6c1obre6q5h2t66vc3l4aji3u8@group.calendar.google.com', timeMin=startOfMonth,
       maxResults=10, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   values = []

   if not events:
       print('No events found.')
   for event in events:
       values.append(event['start'].get('dateTime').split('T'))
       #start = event['start'].get('dateTime', event['start'].get('date'))
       #print(start, event['summary'])

   #print(values)
   return(values)
if __name__ == '__main__':
    main()