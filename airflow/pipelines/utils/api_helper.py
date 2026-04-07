from datetime import datetime

import pendulum


class APIHelper:
    """Helper class to prepare acquisition of data from the API and handle the API data."""

    @staticmethod
    def date_param(dt: datetime) -> pendulum.DateTime:
        """Get the start datetime for data collection.

        :param dt: datetime to be converted to nearest 30 minutes
        :return: datetime
        """
        dt = pendulum.instance(dt)

        # API published data is 90 minutes behind
        return APIHelper.floor_to_30_min(dt).subtract(minutes=90)

    @staticmethod
    def floor_to_30_min(dt: pendulum.DateTime) -> pendulum.DateTime:
        """Floor the given datetime to the nearest 30 minutes.

        :param dt: datetime to be floored
        :return: floored datetime
        """
        return dt.replace(minute=(dt.minute // 30) * 30, second=0, microsecond=0)
