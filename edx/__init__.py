from datetime import date, time
from random import randint
from cockpit.driver.models import WorkSchedule, Driver


WorkSchedule.objects.all().delete()

def create_sch(driver, s1, e1, s2, e2):
    for i in range(1, 31):
        sd = date(2023, 11, i)
        st = time(randint(s1, e1), 0)
        et = time(randint(s2, e2),0)
        WorkSchedule.objects.create(driver=driver, start_time=st, end_time=et, start_date=sd, end_date=sd)


for driver in Driver.objects.all():
    create_sch(driver, 1, 5, 8, 14)
    create_sch(driver, 14, 17, 17, 23)
