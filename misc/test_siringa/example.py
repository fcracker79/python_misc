import siringa


@siringa.register
class Logger:
    def info(self, *a):
        print('Logging ', a)


@siringa.inject
def task_using_class(msg: str, logger: '!Logger'):
    print('task_using_class')
    logger().info(msg)


@siringa.inject
def task_using_a(msg: str, logger: siringa.A('Logger')):
    print('task_using_a')
    logger().info(msg)

task_using_class('hello')
task_using_a('hello')
