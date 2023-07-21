## TrackerInfo
1. python manage.py populate_db (which populates the db given  data)
2. Urls
    1. localhost:8000/swagger/ represents the docs for the endpoints.
    2. localhost:8000/tracker/ (provide a parameter(?device id=20984) and return gives the tracker device location and latest information,distance covered,etc)
    3. localhost:8000/tracker/details/ (provide params device_id,(start_dt=2021-10-23T14:29:03.028049Z end_dt=2021-10-23T14:29:36.526919Z) are optional, returns the latest info of that device given timestamp. )