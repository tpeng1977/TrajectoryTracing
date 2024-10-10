import numpy as np

# Constants
LANE1_LENGTH = 500
LANE2_LENGTH = 500
LANE3_LENGTH = 500
SPEED_LIMIT_LANE1 = 30
SPEED_LIMIT_LANE2_FIRST = 10
SPEED_LIMIT_LANE2_SECOND = 30
SPEED_LIMIT_LANE3 = 30
MAX_SPEED = 35
MIN_DISTANCE = 10
ACCELERATION_LIMIT = 5
TIME_PERIOD = 3600
TIME_STEP = 0.01

# Ball entry rates (balls per second)
ENTRY_RATE_A = 1000 / 3600
ENTRY_RATE_B = 800 / 3600

# Ball types
TYPE_A = 'A'
TYPE_B = 'B'


class Ball:
    def __init__(self, ball_type, entry_time, initial_speed, index):
        self.ball_type = ball_type
        self.index = index
        self.entry_time = entry_time
        self.initial_speed = initial_speed
        self.position = 0
        self.speed = initial_speed
        self.acceleration = 0
        self.traveled_distance = 0
        self.trajectory = []

    def update_position(self, time_step):
        self.speed = min(self.speed + self.acceleration * time_step, MAX_SPEED)
        self.position += self.speed * time_step
        self.traveled_distance += self.speed * time_step
        if len(self.trajectory) == 0:
            self.trajectory.append({'timestamp': self.entry_time, 'traveled_distance': 0.0, 'speed': self.speed})
        self.trajectory.append(
            {'timestamp': self.trajectory[-1]['timestamp'] + time_step, 'traveled_distance': self.traveled_distance,
             'speed': self.speed})


def generate_balls(entry_rate, ball_type, initial_speed):
    balls = []
    time = 0
    index = 0
    while time < TIME_PERIOD:
        time += np.random.exponential(1 / entry_rate)
        if time < TIME_PERIOD:
            balls.append(Ball(ball_type, time, initial_speed, index))
            index += 1
    return balls


def simulate_lane(balls, lane_length, speed_limit, time_step=0.1):
    for i, ball in enumerate(balls):
        t_pos = ball.position
        while ball.position < lane_length + t_pos:
            if i > 0:
                prev_ball = balls[i - 1]
                if prev_ball.position - ball.position < MIN_DISTANCE:
                    ball.speed = min(ball.speed, prev_ball.speed)
                    if ball.speed > 0.0:
                        ball.acceleration = - 0.1
            ball.acceleration = min(ACCELERATION_LIMIT, (speed_limit - ball.speed) / time_step)
            ball.update_position(time_step)


def main():
    # Generate balls for lane 1 and lane 2
    balls_A = generate_balls(ENTRY_RATE_A, TYPE_A, 20)
    balls_B = generate_balls(ENTRY_RATE_B, TYPE_B, 10)

    # Simulate lane 1 for balls of type A
    simulate_lane(balls_A, LANE1_LENGTH, SPEED_LIMIT_LANE1, TIME_STEP)

    # Simulate lane 2 for balls of type B
    for ball in balls_B:
        if ball.position < 200:
            simulate_lane([ball], 200, SPEED_LIMIT_LANE2_FIRST, TIME_STEP)
        simulate_lane([ball], 300, SPEED_LIMIT_LANE2_SECOND, TIME_STEP)

    # Combine balls from lane 1 and lane 2 for lane 3
    all_balls = balls_A + balls_B
    all_balls.sort(key=lambda x: x.entry_time)

    # Simulate lane 3
    simulate_lane(all_balls, LANE3_LENGTH, SPEED_LIMIT_LANE3, TIME_STEP)

    # Output the traveled distance of each ball
    total_distance = 0
    for ball in all_balls:
        total_distance += ball.traveled_distance
        print(
            f"Ball Type: {ball.ball_type} {ball.index}, Traveled Distance: {ball.traveled_distance:.2f} meters, "
            f"average speed: {ball.traveled_distance / (ball.trajectory[-1]['timestamp'] - ball.entry_time)} speed: {ball.trajectory[-1]['speed']}")
        for t_item in ball.trajectory:
            print(f"Ball Type: {ball.ball_type} {ball.index}, timestamp: {t_item['timestamp']}  traveled_distance: {t_item['traveled_distance']}")

    # Calculate and print the average speed
    # average_speed = total_distance / (len(all_balls) * TIME_PERIOD)
    # print(f"Average Speed: {average_speed:.2f} meters/second")


if __name__ == "__main__":
    main()

