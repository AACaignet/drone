broker_url = 'amqp://guest@localhost:5672/'
#result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
#timezone = 'Europe/Oslo'
enable_utc = True
# task_routes = {
#     'tasks.printa': 'low-priority',
# }
# celerybeat_shedule = {
#     'add-every-30-seconds': {
#         'task': 'tareas.tasks.printa',
#         'schedule': 20.0,
#         'args': (16, 16)
#     },
# }