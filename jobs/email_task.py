from base import base_cron_tab
import datetime

class EmailTask(base_cron_tab.BaseCronTab):
    def __init__(self, data):
        super().__init__()
        self.__data = data

    def job(self, data):
        from common.service.email_service import EmailHelper
        email_helper = EmailHelper("")
        for d in data:
            email_helper.receiver = d["address"]
            email_helper.send_email(subject=d["subject"], content=d["content"])

    def schedule(self):
        from utils.scheduler import scheduler
        start_time_bench_mark = datetime.datetime.now()+datetime.timedelta(minutes=1)
        for i in range(0, len(self.__data),10):
            start_time = start_time_bench_mark+datetime.timedelta(seconds=i*30)
            batch_data = self.__data[i:i+10]
            scheduler.add_job(self.job, "date", run_date=start_time,args=[batch_data])