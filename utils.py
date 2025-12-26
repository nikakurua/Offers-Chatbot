from datetime import datetime

def format_date(timestamp_ms):
    if timestamp_ms is None:
        return "მიუთითებელი"
    return datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%d.%m.%Y")

def prepare_offer_text(offer):
    parts = [
        f"სათაური: {offer.get('title','')}",
        f"ბრენდი: {offer.get('brandNames','')}",
        f"ქალაქი: {offer.get('cityNames','')}",
        f"სარგებელი: {offer.get('shortDesc','')}",
        f"ბმული: {offer.get('website') or offer.get('mainPlaceUrl','')}",
        f"პერიოდი: {format_date(offer.get('startDate'))} - {format_date(offer.get('endDate'))}"
    ]
    return "\n".join(parts)
