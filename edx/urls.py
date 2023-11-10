from django.urls import include, path

app_name = 'edx'


urlpatterns = [
    path('chat/', include('edx.chat.urls', namespace='chat')),
    path('courses/', include('edx.courses.urls', namespace='courses')),
    path('students/', include('edx.student.urls', namespace='student')),
    path('courses/api/', include('edx.courses.api.urls', namespace='courses_api')),
]


import re

def find_patterns(string, patterns):
    for pattern, detail in patterns:
        print(f"{pattern=}, {detail=}\n\n'{string}'")
        for match in re.finditer(pattern, string):
            start = match.start()
            end = match.end()
            matched = string[start:end]
            back_slashes = string[:start].count("\\")
            prefix = "." * (start + back_slashes)
            print(f"{prefix}'{matched}'")
        print()


find_patterns('abbaabbba', [
    ('ab*?', 'a followed by zero or more b'),
    ('ab+?', 'a followed by one or more b'),
    ('ab??', 'a followed by zero or one b'),
    ('ab{3}?', 'a followed by three b'),
    ('ab{2,3}?', 'a followed by two to three b')
])