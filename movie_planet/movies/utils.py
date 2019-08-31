from collections import Counter
from datetime import datetime, timedelta


def generate_movie_rank(items):
    counter = Counter(items).most_common()
    result = []

    rank = 0
    for movie_id, total_comments in counter:
        if rank != 0 and counter[rank - 1][1] == total_comments:
            pass
        else:
            rank += 1

        result.append(
            {"movie_id": movie_id, "total_comments": total_comments, "rank": rank}
        )
    return result


def prepare_date_range(from_date, to_date):
    from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_date = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(
        hours=23, minutes=59, seconds=59
    )
    return [from_date, to_date]
