# coding=utf-8
from tornado import ioloop
from bson import ObjectId
import traceback
from collections import defaultdict
from datetime import datetime
from handerBIL.spider_bil import SpiderDashBoardBIL
from DBaction.settings import STATISTIC_PERIOD
from DBaction.redis_action import RedisAction


statistic_table = defaultdict(list)


def check_lock(name):
    def check(func):
        def wrapper():
            r = RedisAction()
            if r.get_period_lock(name):
                try:
                    func()
                except Exception as e:
                    print traceback.print_exc()
                finally:
                    r.del_period_lock(name)
            print "{} done".format(name)
        return wrapper
    return check


def jobs_check_finish(fjob, jobs, bil, job_type):
    finished = len(filter(lambda x: x["status"] == "finished", jobs))
    if float(finished) / len(fjob["servers"]) >= 0.85:
        fjob["status"] = "finished"
        bil.update_many_jobs_status({"job_id": fjob["_id"]}, "finished")
        bil.queue_delete(fjob["_id"])
        fjob = bil.compute_runtime(fjob)
        bil.insert_schedule_history(fjob)
        if job_type not in ["period"]:
            bil.delete_schedule(fjob["_id"])
        print "{} finished".format(fjob["spider_name"])


def jobs_statistic(key, jobs):
    statistic = sum([int(job["item_num"]) for job in jobs])
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if len(statistic_table[key]) >= 30:
        statistic_table[key].pop(0)
    statistic_table[key].append((date, statistic))


@check_lock("jobs_statistic")
def check_finish():
    spider_dashboard = SpiderDashBoardBIL()
    running_jobs = spider_dashboard.get_jobs_without_auth("schedule", {"status": "running"})
    for job in running_jobs:
        job_count = list(spider_dashboard.get_jobs_without_auth("job_running", {"job_id": job["_id"]}))
        key = "{}-{}".format(job["project"], job["spider_name"])
        jobs_statistic(key, job_count)
        jobs_check_finish(job, job_count, spider_dashboard, job["job_type"])
        spider_dashboard.add_job_chart("{}_{}".format(job["_id"], "chart"), statistic_table[key])


if __name__ == '__main__':
    # ioloop.PeriodicCallback(check_finish, STATISTIC_PERIOD).start()  # start scheduler
    # ioloop.IOLoop.instance().start()
    check_finish()
