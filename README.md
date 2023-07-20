## TrackerInfo
1. python manage.py populate_db (which populates the db given  data)
2. Urls
    1. localhost:8000/swagger/ gives the docs
    2. localhost:8000/tracker/ (provide a device id and return gives the tracker device location and latest information )
    3. localhost:8000/tracker/details/ (provide params device_id,(start_dt , end_dt) optional, returns the latest info of that device given timestamp. )