import requests
from django.conf import settings
from django.db.models import Q

from fight_covid19.maps.models import HealthEntry


def get_stats():
    data = dict()
    statewise = dict()  # To store total stats of the state
    statewise_list = []
    last_updated = dict()
    data["sickPeople"] = sick_people = HealthEntry.objects.filter(
        Q(fever=True) | Q(cough=True) | Q(difficult_breathing=True)
    ).count()
    data["totalPeople"] = (
        HealthEntry.objects.all().order_by("user").distinct("user_id").count()
    )
    r = requests.get(settings.COVID19_STATS_API)
    if r.status_code == 200:
        r_data = r.json()
        india_stats = r_data
        total_stats = dict()  # To store total stats of the country
        total_stats.update(india_stats["statewise"][0])
        total_stats["deltaactive"] = india_stats["statewise"][0]["delta"]["active"]
        statewise_list = india_stats["statewise"][1:]
        sorted_list = sorted(
            statewise_list,
            key=lambda i: (int(i["active"]), int(i["confirmed"]), int(i["deaths"])),
            reverse=True,
        )
        for i in sorted_list:
            statewise[i["state"]] = i
            statewise[i["state"]]["deltaactive"] = i["delta"]["active"]

        data.update(total_stats)
        last_updated = india_stats["tested"][-1]
    return data, statewise, last_updated


def get_map_markers():
    points = (
        HealthEntry.objects.all()
        .order_by("user", "-creation_timestamp")
        .distinct("user")
        .values("user_id", "latitude", "longitude")
    )
    return list(points)
