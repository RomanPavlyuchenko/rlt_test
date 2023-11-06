from datetime import datetime


FORMATS = {
    'year': '%Y-01-01T00:00:00',
    'month': '%Y-%m-01T00:00:00',
    'day': '%Y-%m-%dT00:00:00',
    'hour': '%Y-%m-%dT%H:00:00',
    'minute': '%Y-%m-%dT%H:%M:00',
    'second': '%Y-%m-%dT%H:%M:%'
}


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
                            'format': FORMATS[group_type],
                            'date': '$dt'
                        }
                    }
                },
                'total': {'$sum': "$value"}
            }
        },
        {
           '$sort': {'_id': 1}
        },
        {
            '$group': {
                '_id': None,
                'dataset': {'$push': '$total'},
                'labels': {'$push': '$_id.date'}
            }
        },
        {
            '$project': {
                '_id': 0,
                'dataset': 1,
                'labels': 1
            }
        },

    ]
    return pipeline
