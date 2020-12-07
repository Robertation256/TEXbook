from base import base_cron_tab

class RecoverUnlockChanceTask(base_cron_tab.BaseCronTab):

    def job(self):
        from addons.user.model.user import User
        User.recover_unlock_chance()

    def schedule(self):
        from utils.scheduler import scheduler
        scheduler.add_job(self.job, "cron", hour=0, minute=0, second=0)