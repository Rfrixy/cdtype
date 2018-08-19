// entering a new score

dept key:
0: Tech
1: Mobile
2: Hr
3: Content
4: Email


db.scores.insert({name:'Divesh Naidu', email:'divesh.naidu@collegedunia.com', speed:45, achieved_on: new Date(),dept:})
db.scores.insert({name:'Sudhansh Jayant', email:'sudhansh.jayant@3dot14.co', speed:45, achieved_on: new Date(),dept:"Mobile"})
db.scores.insert({name:'Prince Sehrawat', email:'prince.s@collegedunia.com', speed:35, achieved_on: new Date(),dept:"Tech"})

db.scores.update({name:'Divesh Naidu'}, {$set:{speed:a a a, achieved_on: new Date()}})


db.scores.update({name:'Divesh Naidu'}, {$set:{dept:"Tech"}})
