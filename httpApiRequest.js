const https = require("https");
const url = "https://sv443.net/jokeapi/v2/joke/Any?type=single";

https.get(url, res => {
  res.setEncoding("utf8");
  let body = "";
  res.on("data", data => {
    body += data;
  });
  res.on("end", () => {
    body = JSON.parse(body);
    console.log(body);
    console.log(body.joke);
  });
});