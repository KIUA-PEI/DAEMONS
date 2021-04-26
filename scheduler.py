from apscheduler.schedulers.background import BackgroundScheduler
import time

# jobs
def hour_job():
    print("this job runs every 1 hour")

def ten_sec_job():
    print("this job runs every 10 sec")

def thirty_sec_job():
    print("this job runs every 30 sec")


def main():
    print("runs main")
    # start scheduler
    scheduler = BackgroundScheduler()
    
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    # cuidado com a timezone
    scheduler.configure(job_defaults=job_defaults)

    # add jobs
    scheduler.add_job(hour_job, trigger="interval", hours=1, id="1hourjob")
    scheduler.add_job(ten_sec_job, trigger="interval", seconds=10, id="10secjob")
    scheduler.add_job(thirty_sec_job, trigger="interval", seconds=30, id="30secjob")

    # start the scheduler
    scheduler.start()

    try:
        while True:
            # simulate activity (which keeps the main thread alive)
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("exiting...")
        scheduler.shutdown()

if __name__=="__main__":
    main()