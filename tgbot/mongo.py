from datetime import datetime


def get_pipeline(
        date_from: str = '2022-09-01T00:00:00',
        date_to: str = '2022-12-31T23:59:59',
        group_type: str = 'month'):

    start_datetime = datetime.strptime(date_from, '%Y-%m-%dT%H:%M:%S')
    end_datetime = datetime.strptime(date_to, '%Y-%m-%dT%H:%M:%S')

    pipeline = [
        {
            '$match': {
                'dt': {
                    '$gte': start_datetime,
                    '$lte': end_datetime
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'date': {
                        '$dateToString': {
                            'format': "%Y-%m-01T00:00:00", 'date': "$dt"
                        }
                    }
                },
                'sum': {'$sum': "$value"}
            }
        }
    ]
    return pipeline
