
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore

scheduler = BackgroundScheduler()
jobstore = RedisJobStore(host="127.0.0.1",port=6379)

scheduler.add_jobstore(jobstore)
