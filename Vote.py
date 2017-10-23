def startVote(message):
    try:
        pilkku = 0
        votes = []
        choices = message.split('!startvote ', 1)
        choices = choices[1]
        for sana in choices:
            if "," in sana:
                pilkku = 1
        if pilkku == 1:
            choices = map(str.strip, choices.split(","))
        else:
            choices = map(str.strip, choices.split(" "))

        for i in range(len(choices)):
            votes.append(0)

        return choices, votes


    except Exception, e:
        print "inside startvote error:", e


def addVote(choices, votes, message):
    try:
        msg = message.split('!vote ', 1)
        toVote = msg[1]
        try:
            if int(toVote) > 0:
                num = votes[int(toVote) - 1]
                num = num + 1
                votes[int(toVote) - 1] = num
        except:
            try:
                i = choices.index(toVote)
                num = votes[i]
                num = num + 1
                votes[i] = num
            except Exception, e:
                print "addvote error:",e

        return votes

    except Exception, e:
        print "addvote error:", e


def endVote(choices, votes):
    try:
        a = max(votes)
        winners = ""
        winlist = []
        mostvotes = [i for i, j in enumerate(votes) if j == a]
        for i in mostvotes:
            winlist.append(choices[i])
            winlist.append(" (")
            winlist.append(str(votes[i]))
            winlist.append(")")
            winlist.append(", ")
        winlist.pop()
        winners = "".join(winlist)
        return winners

    except Exception, e:
        print "endvote error:", e
