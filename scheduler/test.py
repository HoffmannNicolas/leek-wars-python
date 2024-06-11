from scheduler import Scheduler
from task import Task

task1 = Task(1.0)
task2 = Task(2.0)
task3 = Task(3.0)

scheduler = Scheduler([task1, task2, task3])
scheduler.run_next_task()


scheduler.run()
