import requests


import datetime
import re


def backouts(tree, start_date, end_date):
    if tree.startswith('comm-'):
        return None
    total_pushes = requests.get("https://hg.mozilla.org/%s/json-pushes?full=1&startdate=%s&enddate=%s" %
        ("integration/%s" % tree if tree != "mozilla-central" else tree, start_date, end_date), verify=True).json()
    backed = 0
    backoutln = re.compile('^.*[b,B]ackout.*')
    backoutln2 = re.compile('^.*[b,B]acked out.*')
    backoutln3 = re.compile('^.*[b,B]ack out.*')
    merges = re.compile('^.*[M,m]erge .* to .*')
    keys_to_pop = []
    for resp in total_pushes:
        for chnge in range(len(total_pushes[resp]['changesets'])):
            if merges.match(total_pushes[resp]['changesets'][chnge]['desc']):
                keys_to_pop.append(resp)

    for key in keys_to_pop:
        total_pushes.pop(key, None)

    import pdb; pdb.set_trace()
    backout_hours = [0] * 24
    pushes_hours = [0] * 24

    for resp in total_pushes:
        # Lets also track what hour the push happened in
        bhour = datetime.datetime.fromtimestamp(int(total_pushes[resp]['date'])).hour
        pushes_hours[bhour] = pushes_hours[bhour] + 1
        for chnge in range(len(total_pushes[resp]['changesets'])):
            if (backoutln.match(total_pushes[resp]['changesets'][chnge]['desc']) or
                backoutln2.match(total_pushes[resp]['changesets'][chnge]['desc']) or
                backoutln3.match(total_pushes[resp]['changesets'][chnge]['desc'])):
                backed += 1

                # Lets also track what hour the backouts happened in
                bhour = datetime.datetime.fromtimestamp(int(total_pushes[resp]['date'])).hour
                backout_hours[bhour] = backout_hours[bhour] + 1
                break

    return {"total": len(total_pushes),
            "backouts": backed,
            "startdate": start_date,
            #"pushes": total_pushes,
            "backoutHours": backout_hours,
            "pushesHours": pushes_hours}

if __name__ == '__main__':
    print backouts('autoland', '2017-02-01', '2017-02-28')
