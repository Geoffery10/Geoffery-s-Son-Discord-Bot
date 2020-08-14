const fs = require('fs')
const path = './memberData.json'
var undef;
var members;

var member = {
    user:"QSteven", 
    userID:"246263645346", 
    sins:"Many"
};

const loadJson = function () {
    let rawdata = fs.readFileSync(path);
    let members = JSON.parse(rawdata);
    return members
} 

const saveJson = function(member) {
    console.log("Pushing new member: " + JSON.stringify(member, null, 4))
    fs.readFile(path, function (err, data) {
        var json = JSON.parse(data)
        json.push(member)
        
        fs.writeFileSync(path, JSON.stringify(json, null, 4))
    })
}

const checkMember = async function(userSent, userIDSent) {
    members = loadJson()
    member = members.find( ({ userID }) => userID === userIDSent )
    if (member == undef) {
        member = {
            user:userSent, 
            userID:userIDSent, 
            sins:"Sinless... for now..."
        }
        //members.push(member)
        saveJson(member)
        members.push(member)
    }
    //console.log(member);

    return member
}

module.exports.checkMember = checkMember;