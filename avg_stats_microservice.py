import zmq
from datetime import datetime
import time

def get_stats(timeframe, data):
    activities = 0
    distance = 0
    time = 0
    elevation_gain = 0
    if timeframe == "MONTH":
        current_date = datetime.now().date()
        for activity in data:
            activity_date = datetime.strptime(activity['date'], '%Y-%m-%d').date()
            diff = current_date - activity_date
            if diff.days <= 28:
                activities += 1
                distance += activity['distance']
                time += activity['duration']
                elevation_gain += activity['elevation']
    activities = activities / 4
    distance = distance / 4
    time = time / 4
    elevation_gain = elevation_gain / 4

    return {'activities': activities, 'distance': distance, 'duration': time, 'elevation': elevation_gain}
def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5557")

    print("Listening for requests...")
    while True:
        request = socket.recv_json()
        stats = get_stats(request['time'], request['data'])
        print(f"Retrieving average stats for {request['time']}...")
        print(stats)
        socket.send_json(stats)

if __name__ == '__main__':
    main()
