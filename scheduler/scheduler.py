

from task import Task


class Scheduler():

    """ This scheduler executes repeating tasks in order, each task with a different interval.
    It does is be keeping a list of the tasks to be executed sorted by their next execution time.
    After each execution, the task is rescheduled with the current time + the interval."""

    def __init__(self, tasks=[]):

        self.tasks = []
        self.time = 0.0

        for task in tasks:
            self.schedule(task)


    def tasks_are_waiting(self):

        """ Return True if there are tasks waiting to be executed. """

        return len(self.tasks) > 0


    def tasks_are_over(self):

        """ Return True if there are no more tasks to be executed. """

        return not(self.tasks_are_waiting())


    def run(self, timeout=1e3):

        """ Run all tasks until they are over. """

        while self.tasks_are_waiting():

            self._run_next_task()

            if self.time > timeout:
                print("Timeout!")
                break


    def run_n_tasks(self, n):

        """ Run up to n tasks. """

        for _ in range(n):

            if self.tasks_are_over():
                break

            self._run_next_task()


    def _run_next_task(self):

        """ Run the next task that is due, if any. """

        task = self.tasks.pop(0)
        self.time = task.next_run
        task.run()

        self.schedule(task)


    def schedule(self, task):

        """ Schedule a task for execution. """

        assert isinstance(task, Task), "task must be a Task object"

        task.next_run = self.time + task.get_interval()

        self.tasks.append(task)
        self.tasks.sort(key=lambda task: task.next_run)
