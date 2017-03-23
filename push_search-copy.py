import requests


import datetime
import re


def backouts(tree, start_date, end_date):
    if tree.startswith('comm-'):
        return None
    total_pushes = requests.get("https://hg.mozilla.org/%s/json-pushes?full=1&startdate=%s&enddate=%s" %
        ("integration/%s" % tree if tree != "mozilla-central" else tree, start_date, end_date), verify=True).json()
    backed = 0
    backoutln = re.compile('^.*[b,B]acked out.*')
    merges = re.compile('^.*[M,m]erge .* to .*')
    bug = re.compile('^([b,B]ug (\d+))')
    keys_to_pop = []
    backouts = 0
    servo_pushes = 0
    multi_bug_push = []
    total_bugs = 0
    total_changesets = 0
    total_changesets_without_servo = 0
    for resp in total_pushes:
        is_merge = False
        bug_nums = []
        total_changesets += len(total_pushes[resp]['changesets'])
        if total_pushes[resp]['user'] != "servo-vcs-sync@mozilla.com":
            total_changesets_without_servo += len(total_pushes[resp]['changesets'])
        for chnge in range(len(total_pushes[resp]['changesets'])):

            commit_msg = total_pushes[resp]['changesets'][chnge]['desc']
            bug_num = re.search(bug, commit_msg)

            if bug_num is not None:
                bug_nums.append(bug_num.group(2))
            if resp == '36946':
                print("'{}'".format(commit_msg))
                #import pdb; pdb.set_trace()
            if merges.search(commit_msg):
                is_merge = True
                keys_to_pop.append(resp)
                total_changesets = total_changesets - len(total_pushes[resp]['changesets'])
                total_changesets_without_servo = total_changesets_without_servo - len(total_pushes[resp]['changesets'])
                break
            if (backoutln.match(commit_msg)):
                backouts += 1
                break

        if len(set(bug_nums)) > 1 and resp not in keys_to_pop:
            #import pdb; pdb.set_trace()
            #print("push: {} pusher: {}".format(resp, total_pushes[resp]['user']))
            #for chnge in range(len(total_pushes[resp]['changesets'])):
            #    print("** {}".format(total_pushes[resp]['changesets'][chnge]['desc']))
            multi_bug_push.append(resp)
        total_bugs += len(set(bug_nums))
        if total_pushes[resp]['user'] == "servo-vcs-sync@mozilla.com":
            servo_pushes = servo_pushes + 1

    for key in keys_to_pop:
        total_pushes.pop(key, None)

    print("*****************{0}*****************".format(tree))
    print("Total Servo Sync Pushes: {0}".format(servo_pushes))
    print("Total Pushes: {0}".format(len(total_pushes.keys())))
    print("Total Number of commits {0}".format(total_changesets))
    print("Total number of commits without Servo {0}".format(total_changesets_without_servo))
    print("Total Backouts: {0}".format(backouts))
    print("Total of Multi-bug pushes {0}".format(len(multi_bug_push)))
    print("Total number of bugs changed {0}".format(total_bugs))
    print("Percentage of backout against bugs: {0}".format(100 * float(backouts)/float(total_bugs)))
    print("Percentage of backouts: {0}".format(100 * float(backouts)/float(len(total_pushes.keys()))))
    print("Percentage of backouts without Servo: {0}".format(100 * float(backouts)/float(len(total_pushes.keys())-servo_pushes)))


if __name__ == '__main__':
    backouts('autoland', '2017-02-01', '2017-03-10')
#    backouts("mozilla-inbound", '2017-02-01', '2017-03-10')
