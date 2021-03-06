import bugsy

import datetime
import collections

def get_intermittents_created_in_last(days=7):
    tday = datetime.date.today()
    tday_minus_7 = date_as_of(days)
    today = '%s-%s-%s' %(tday.year, tday.month if tday.month >= 10 else '0%s' % tday.month, tday.day)
    seven_days_ago = '%s-%s-%s' %(tday_minus_7.year, tday_minus_7.month if tday_minus_7.month >= 10 else '0%s' % tday_minus_7.month, tday_minus_7.day)
    bugzilla = bugsy.Bugsy()
    return bugzilla.search_for\
                   .keywords("intermittent-failure")\
                   .change_history_fields(['[Bug creation]'])\
                   .timeframe(seven_days_ago, today)\
                   .search()

def get_intermittents_closed(days=7):
    tday = datetime.date.today()
    tday_minus_7 = date_as_of(days)
    today = '%s-%s-%s' %(tday.year, tday.month if tday.month >= 10 else '0%s' % tday.month, tday.day)
    seven_days_ago = '%s-%s-%s' %(tday_minus_7.year, tday_minus_7.month if tday_minus_7.month >= 10 else
                 '0%s' % tday_minus_7.month, tday_minus_7.day)
    bugzilla = bugsy.Bugsy()
    bugs = bugzilla.search_for\
                   .keywords("intermittent-failure")\
                   .change_history_fields(['bug_status'], 'Resolved')\
                   .timeframe(seven_days_ago, today)\
                   .search()
    result= {}
    for bug in bugs:
        try:
            result[bug.resolution] = result[bug.resolution] + 1
        except:
            result[bug.resolution] = 1

    for k,v in result.iteritems(): 
        print "%s: %s" % (k, v)

def date_as_of(days):
    tday = datetime.datetime.today()
    return tday - datetime.timedelta(days=days)

def amount_of_comments_per_bug():
    bugs = get_intermittents_created_in_last(120)
    comment_breakdown = {}
    ready_to_close = []
    thirty_days = date_as_of(30)
    for bug in bugs:
        if bug.product == "Thunderbird" \
            or bug.status.upper() == "RESOLVED"\
            or "[leave open]" in bug._bug["whiteboard"] \
            or "orange-bomb" in bug._bug["whiteboard"]:
            continue
        comments = bug.get_comments()

        delta = thirty_days - comments[-1].creation_time
        if len(comments) in comment_breakdown:
            if len(comments) <= 2 and delta.days >= 0:
                ready_to_close.append(bug.id)

            comment_breakdown[len(comments)].append(bug.id)
        else:
            if len(comments) <= 2 and delta.days >= 0:
                ready_to_close.append(bug.id)
            comment_breakdown[len(comments)] = [bug.id]

    ordered_breakdown = collections.OrderedDict(sorted(comment_breakdown.items()))
    for count, bug_array in ordered_breakdown.iteritems():
        pass
        print("Bugs %s had %s comments" % (bug_array, count))

    print("The following bugs can be closed %s" % ready_to_close)


def bugs_possibly_ready_to_close():
    bugs = get_intermittents_created_in_last(120)
    ready_to_close = []
    bugs_to_review = []
    fortyfive_days = date_as_of(45)
    for bug in bugs:
        if bug.product == "Thunderbird" \
            or bug.status.upper() == "RESOLVED" \
            or "[leave open]" in bug._bug["whiteboard"]\
            or "orange-bomb" in bug._bug["whiteboard"]:
            continue
        comments = bug.get_comments()

        delta = fortyfive_days - comments[-1].creation_time
        if "tbpl" in comments[-1].author and delta.days >= 0:
            ready_to_close.append(bug.id)
            for comment in comments:
                if "disabled" in comment.text.lower():
                    bugs_to_review.append(bug.id)
                    break

    print("The following bugs can be closed %s" % ready_to_close)
    print("*****************************************************")
    print("The following bugs need to be reviewed %s" % set(bugs_to_review))

if __name__ == '__main__':
    #bugs_possibly_ready_to_close()
    #amount_of_comments_per_bug()
    get_intermittents_closed(120)
