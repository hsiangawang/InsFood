const express = require('express')
const app = express();
const mongoose = require('mongoose');
const passport = require('passport');
const passportLocalMongoose = require('passport-local-mongoose');
const LocalStrategy = require('passport-local');
const bodyParser = require("body-parser");

const port = 3000;
// Connect to mongoDB cluster
const mongo_connection = "mongodb+srv://Adam:XDBoost@cluster0.clmro.mongodb.net/user_auth?retryWrites=true&w=majority"
mongoose.connect(mongo_connection, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('Connected to DB!'))
.catch(error => console.log(error.message));


app.set('view engine', 'ejs');

app.get("/", (req, res) => {
    res.render("home");
});

app.get('/secret', (req, res) => {
    res.render("secret");
})


app.listen(port, ()=> {
    console.log("Start Connection");
});