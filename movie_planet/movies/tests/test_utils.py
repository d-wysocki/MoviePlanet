from movie_planet.movies.utils import generate_movie_rank,prepare_date_range
from datetime import datetime, timedelta


class TestUtils:

    def test_generate_movie_rank(self):
        movies_ids = [1,1,1,1,1,2,2,2,2,2,3,3,4]
        result = generate_movie_rank(movies_ids)

        assert result == [
            {'movie_id': 1,'total_comments': 5,'rank': 1,},
            {'movie_id': 2,'total_comments': 5,'rank': 1,},
            {'movie_id': 3,'total_comments': 2,'rank': 2,},
            {'movie_id': 4,'total_comments': 1,'rank': 3},
        ]

    def test_prepare_date_range(self):
        from_date = "1993-03-11"
        to_date = "1993-03-11"
        expected_from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        expected_to_date = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(
        hours=23, minutes=59, seconds=59
    )
        result = prepare_date_range(from_date,to_date)

        assert result == [expected_from_date,expected_to_date]
