// entering a new score

dept key:
0: Tech
1: Mobile
2: Hr
3: Content
4: Email


db.scores.insert({name:'Divesh Naidu', email:'divesh.naidu@collegedunia.com', speed:45, achieved_on: new Date(),dept:})
db.scores.insert({name:'Sudhansh Jayant', email:'sudhansh.jayant@3dot14.co', speed:45, achieved_on: new Date(),dept:"Mobile"})

db.scores.insert({name:'Nikhil Kumar', email:'nikhil.kumar@collegedunia.com', speed:65, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Rohit Singh', email:'rohit.singh@collegedunia.com', speed:26, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Raviranjan Singh', email:'ravi.ranjan@3dot14.co', speed:40, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Kanhaiya Murarka', email:'Kanhaiya.Murarka@collegedunia.com', speed:45, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Simant Saurav', email:'Simant.Saurav@collegedunia.com', speed:41, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Anant Gupta', email:'anant.gupta@collegedunia.com', speed:36, achieved_on: new Date(),dept:"Operations"})
db.scores.insert({name:'Jayant Pratap', email:'Jayant.Pratap@collegedunia.com', speed:43, achieved_on: new Date(),dept:"Tech"})



db.scores.insert({name:'Rexy Joseph', email:'rexy.joseph@collegedunia.com', speed:52, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Akanksha Singh', email:'akanksha@collegedunia.com', speed:53, achieved_on: new Date(),dept:"Email"})
db.scores.insert({name:'Atul Kumar', email:'atul.kumar@collegedunia.com', speed:25, achieved_on: new Date(),dept:"Tech"})
db.scores.insert({name:'Gauren Bhardwaj', email:'gauren.bhardwaj@collegedunia.com', speed:45, achieved_on: new Date(),dept:"Product"})
db.scores.insert({name:'Sakshi Sharma', email:'sakshi.sharma@collegedunia.com', speed:46, achieved_on: new Date(),dept:"Mobile"})
db.scores.insert({name:'Sudhansh Jayant', email:'sudhansh.jayant@collegedunia.com', speed:73, achieved_on: new Date(),dept:"Mobile"})
db.scores.insert({name:'Urvi Setia', email:'urvi.setia@3dot14.co', speed:31, achieved_on: new Date(),dept:"Mobile"})
db.scores.insert({name:'Chandrakant', email:'chandrakant.j@collegedunia.com', speed:47, achieved_on: new Date(),dept:"SEO"})
db.scores.insert({name:'Rishabh Thakur', email:'rishabh.thakur@3dot14.co', speed:53, achieved_on: new Date(),dept:"Graphic"})
db.scores.insert({name:'Aneesh Uppal', email:'aneesh.uppal@collegedunia.com', speed:78, achieved_on: new Date(),dept:"Product"})
db.scores.insert({name:'Anamika Mahajan', email:'anamika.mahajan@collegedunia.com', speed:19, achieved_on: new Date(),dept:"Content"})



db.scores.update({name:'Divesh Naidu'}, {$set:{speed:85, achieved_on: new Date()}})
db.scores.update({name:'Aneesh Uppal'}, {$set:{speed:85, achieved_on: new Date()}})

db.scores.update({name:'Raviranjan Singh'}, {$set:{speed:66, achieved_on: new Date()}})
db.scores.update({name:'Raviranjan Singh'}, {$set:{speed:66, achieved_on: new Date()}})


db.scores.update({name:'Divesh Naidu'}, {$set:{dept:"Tech"}})



db.texts.insert({text:"I'm just not the guy for you. I mean, you need a guy who's happy and perky all the time. Maybe a guy who's had part of his brain removed and he thinks he's a bunny and you can go off and be bunnies together."})
db.texts.insert({text:"In the short term, it would make me happy to go play outside. In the long term, it would make me happier to do well at school and become successful. But in the very long term, I know which will make better memories."})
db.texts.insert({text:"I suggest you change your diet. It could lead to high blood pressure if you fry it. Or even a stroke, heart attack, heart disease."})
db.texts.insert({text:"Confession is not betrayal. What you say or do doesn't matter; only feelings matter. If they could make me stop loving you - that would be the real betrayal."})
db.texts.insert({text:"I love the ground under his feet, and the air over his head, and everything he touches and every word he says. I love all his looks, and all his actions and him entirely and all together."})
db.texts.insert({text:"For centuries, the battle of morality was fought between those who claimed that your life belongs to God and those who claimed that it belongs to your neighbors. And no one came to say that your life belongs to you and that the good is to live it."})
db.texts.insert({text:"Suddenly quite near him there was a rifle shot. He heard the crack and smack and whistling ricochet among the rocks behind him. He dropped his torch and began feebly to trot."})
db.texts.insert({text:"Something in the wind has learned my name and it's telling me that things are not the same. In the leaves on the trees and the touch of the breeze there's a pleasing sense of happiness for me."})
db.texts.insert({text:"Certain things, they should stay the way they are. You ought to be able to stick them in one of those big glass cases and just leave them alone."})
db.texts.insert({text:"The hills are alive with the sound of music, with songs they have sung for a thousand years. The hills fill my heart with the sound of music. My heart wants to sing every song it hears."})
db.texts.insert({text:"A long time ago, I can still remember how that music used to make me smile, and I knew if I had my chance that I could make those people dance and maybe they'd be happy for a while."})
db.texts.insert({text:"I close my eyes only for a moment, and the moment's gone. All my dreams pass before my eyes, a curiosity. Dust in the wind, all they are is dust in the wind."})
db.texts.insert({text:"There is only one wish on my mind: when this day is through I hope that I will find that tomorrow will be just the same for you and me. All I need will be mine if you are here."})
db.texts.insert({text:"I can't believe the things I see. The path that I have chosen now has led me to a wall, and with each passing day I feel a little more like something dear was lost."})
db.texts.insert({text:"You must love your work, and not be always looking over the edge of it, wanting your play to begin. And the other is, you must not be ashamed of your work, and think it would be more honorable to you to be doing something else."})
db.texts.insert({text:"I find myself so furious at all these people that I am in contact with just for controlling me or whatever but you know they are not even aware they are doing it."})
db.texts.insert({text:"I appreciate but can't accept this thank you note that's sealed with your last breath, and I won't stand aside and listen to you give up."})
db.texts.insert({text:"Think of what you're saying, you can get it wrong and still you think that it's alright. Think of what I'm saying, we can work it out and get it straight or say good night."})
db.texts.insert({text:"We used to look at the stars and confess our dreams, hold each other till the morning light. We used to laugh, now we only fight. Baby, are you lonesome now?"})
db.texts.insert({text:"She can lead you to love, she can take you or leave you, she can ask for the truth, but she'll never believe. And she'll take what you give her as long as it's free."})
