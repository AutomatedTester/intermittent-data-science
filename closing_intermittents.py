import bugsy
import requests


if __name__ == '__main__':
    # Let's search for intermittents
    bz = bugsy.Bugsy(api_key="hahahahahah")
    intermittents = bz.search_for.component("marionette").keywords("intermittent-failure").search()
    open_intermittents = [intermittent for intermittent in intermittents if intermittent.status != "RESOLVED" and intermittent.to_dict()["whiteboard" != "test disabled"]

    # Let's see if they have been seen on OF for a while
    to_be_closed = []
    for inter in open_intermittents:
        res = requests.get("https://brasstacks.mozilla.com/orangefactor/api/bybug?startday=2017-01-14&endday=2017-03-21&bugid={}".format(inter.id)).json()
        oranges = 0
        for k, v in res["oranges"].iteritems():
            oranges += v["orangecount"]
        # print("Bug id: {} has had {} oranges".format(inter.id, oranges))
        if oranges == 0:
            to_be_closed.append(inter)

    # Let's close some of them
    print("{} bugs to be closed".format(len(to_be_closed)))
    for bug in to_be_closed:
        bug.add_comment("Closing as intermittent has not been seen in last 45 days")
        bug.status = "RESOLVED"
        bug.resolution = "WORKSFORME"
        bz.put(bug)
        print("Bug {} has been closed".format(bug.id))
