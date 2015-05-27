import bugsy
import time


BUGS_TO_CLOSE = []
USERNAME = ""
PASSWORD = ""

def close_bugs():
    if len(BUGS_TO_CLOSE) == 0:
        print("No Bugs that need closing")
        return

    bugzilla = bugsy.Bugsy(USERNAME, PASSWORD)
    for bug in BUGS_TO_CLOSE:
        try:
            bz_bug = bugzilla.get(bug)
            bz_bug.add_comment("[Mass Closure] Closing Intermittent as a one off")
            bz_bug.status = 'RESOLVED'
            bz_bug.resolution = 'WORKSFORME'
            bugzilla.put(bz_bug)
            print("%s has been closed" % bz_bug.id)
        except:
            print "%s has not been closed" % bug

        time.sleep(10)

if __name__ == "__main__":
    close_bugs()
