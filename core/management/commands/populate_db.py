from django.core.management.base import BaseCommand
from pathlib import Path
import os
import csv
from core.models import VehicleLocation
from dateutil.parser import isoparse
from tqdm import tqdm
from django.core.cache import cache


class Command(BaseCommand):
    help = "Sort the data with respect to sts column and populate in db(postgres)"
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def validate_db(self):
        data_count = VehicleLocation.objects.all().count()
        if data_count > 0:
            VehicleLocation.objects.all().delete()
        return True

    def handle(self, *args, **kwargs) -> None:
        check_db_stats = self.validate_db()
        if check_db_stats:
            with open(os.path.join(self.BASE_DIR, "data", "raw-data.csv")) as data:
                data_reader = csv.reader(data)
                header = next(data_reader)
                # sort the data on sts.
                sorted_data = sorted(data_reader, key=lambda row: row[4], reverse=True)
                progress_bar = tqdm(
                    total=len(sorted_data), desc="Ingesting postgres data", unit="item"
                )
                for idx, curr_data in enumerate(sorted_data):
                    device_id, lat, long, ts, sts, speed = curr_data
                    vehicle = VehicleLocation()
                    vehicle.device_id = int(device_id)
                    vehicle.lat = float(lat)
                    vehicle.long = float(long)
                    vehicle.ts = isoparse(ts)
                    vehicle.sts = isoparse(sts)
                    vehicle.speed = int(speed)
                    vehicle.save()
                    progress_bar.update(1)
                progress_bar.close()

            # store it in redis(cache) for faster retrieval
            unique_device_ids = VehicleLocation.objects.values_list(
                "device_id", flat=True
            ).distinct()
            progress_bar_redis = tqdm(
                total=len(unique_device_ids), desc="Ingesting redis data", unit="item"
            )
            for curr_id in unique_device_ids:
                # top latest records sliced to [:100] if removed it will ingest all redis
                top_latest = VehicleLocation.objects.filter(device_id=curr_id).order_by(
                    "-sts"
                )
                exclude_keys = ["_state", "id"]
                latest_data = []
                for curr_redis_data in top_latest:
                    d = curr_redis_data.__dict__
                    result = {k: d[k] for k in set(list(d.keys())) - set(exclude_keys)}
                    latest_data.append(result)
                print(latest_data)
                print("latest_data")
                cache.set(str(curr_id), latest_data)
                print("after set")
                print(cache.get(str(curr_id)))
                progress_bar_redis.update(1)
            progress_bar_redis.close()
