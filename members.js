const fs = require('fs')
const path = './memberData/memberData.json'
var undef;
var members;

var member = {
    user:"QSteven", 
    userID:"246263645346", 
    sins:"Many",
    anime: 0
};

const loadJson = function () {
    let rawdata = fs.readFileSync(path);
    let members = JSON.parse(rawdata);
    return members
} 

const addScore = function (userSent, userIDSent, score, member) {
    member = {
        user:userSent, 
        userID:userIDSent, 
        sins:member.sins,
        score: (member.score + score)
    }
    //members.push(member)
    updateMembers(member, members)
    //console.log(member);

    return member
}

function updateMembers(member, members){
    var i;
    for (i = 0; i < members.length; ++i) {
      if (members[i].userID == member.userID) {
        members[i].score = member.score;
      }
    }
    fs.writeFileSync(path, JSON.stringify(members, null, 4));
    return members;
  }

const saveJson = function(member) {
    console.log("Pushing new member: " + JSON.stringify(member, null, 4))
    fs.readFile(path, function (err, data) {
        var json = JSON.parse(data)
        json.push(member)
        
        fs.writeFileSync(path, JSON.stringify(json, null, 4))
    })
}

const checkMember = function(userSent, userIDSent) {
    console.log(`Adding ${userSent} to memeber list.`)
    members = loadJson()
    member = members.find( ({ userID }) => userID === userIDSent )
    if (member == undef) {
        member = {
            user:userSent, 
            userID:userIDSent, 
            sins:"Sinless... for now...",
            score: 0
        }
        //members.push(member)
        saveJson(member)
        members.push(member)
    }
    //console.log(member);

    return member
}

module.exports.checkMember = checkMember;
module.exports.addScore = addScore;