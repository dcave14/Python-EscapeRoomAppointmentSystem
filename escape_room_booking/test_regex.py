import re

def test_time_regex():
    pattern = r'^(0?[1-9]|1[0-2]):\d{2} (AM|PM)$'
    time_strings = ['09:00 AM', '12:30 PM', '9:45 AM', '10:00 PM', '25:00 AM', '09:00', 'AM 09:00']

    for time_str in time_strings:
        if re.match(pattern, time_str):
            print(f"Match: {time_str}")
        else:
            print(f"No match: {time_str}")

if __name__ == '__main__':
    test_time_regex()