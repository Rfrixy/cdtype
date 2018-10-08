def matchUsers(db,res):
    # print("I was called")
    # print(db)
    # print(res)
    data = db.scores.find({'averages':{'$exists':1}},{'name':1,'averages':1})
    data = list(data)
    print(data)
