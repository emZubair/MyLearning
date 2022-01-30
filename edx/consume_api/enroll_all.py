import requests


BASE_URL = 'http://127.0.0.1:8000/edx/courses/api/'

# retrieve all courses

response = requests.get(f'{BASE_URL}courses/')

courses = response.json()
available_courses = ', '.join(course['title'] for course in courses)

print(f'Available courses: {available_courses}')

for course in courses:
    course_id = course['id']
    course_title = course['title']
    res = requests.post(f'{BASE_URL}courses/{course_id}/enroll/', auth=('gul', 'admin12345'))
    if res.status_code == 200:
        print(f"Successfully enrolled in :{course_title}")
    else:
        print(f"Failed to enroll in: {course_title}")

