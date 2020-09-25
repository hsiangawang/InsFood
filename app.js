const express = require('express')
const mongoose = require('mongoose');
const passport = require('passport');
const passportLocalMongoose = require('passport-local-mongoose');
const LocalStrategy = require('passport-local');
const bodyParser = require("body-parser");
const User = require('./models/user')

const port = 3000;

var app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended: true}));

// Connect to MySQL DB
var mysql = require('mysql');

var mysql_connection = mysql.createConnection({
  host     : "insfood-database.cotdjnfrrj8j.us-east-2.rds.amazonaws.com",
  database : "InsFood",
  user     : "admin",
  password : "xddd1234",
  port     : 3306
});

mysql_connection.connect(function(err) {
  if (err) {
    console.error('Database connection failed: ' + err.stack);
    return;
  }

  console.log('Connected to database.');
});

mysql_connection.end();

// Connect to mongoDB cluster
const mongo_connection = 'mongodb+srv://Adam:XDBoost@cluster0.clmro.mongodb.net/user_auth?retryWrites=true&w=majority'
mongoose.connect(mongo_connection, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('Connected to DB!'))
.catch(error => console.log(error.message));

app.use(require("express-session")({
    secret: "XDBoost",
    resave: false,
    saveUnitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());


app.get('/', (req, res) => {
    res.render('home');
});

app.get('/secret', isLoggedIn, (req, res) => {
    res.render('secret');
})

// Auth Routes

//show sign up form
app.get("/register", function(req, res){
    res.render("register"); 
 });
 //handling user sign up
 app.post("/register", function(req, res){
     User.register(new User({username: req.body.username}), req.body.password, function(err, user){
         if(err){
             console.log(err);
             return res.render('register');
         }
         passport.authenticate("local")(req, res, function(){
            res.redirect("/secret");
         });
     });
 });

 // LOGIN ROUTES
//render login form
app.get("/login", function(req, res){
    res.render("login"); 
 });
 //login logic
 //middleware
 app.post("/login", passport.authenticate("local", {
     successRedirect: "/secret",
     failureRedirect: "/login"
 }) ,function(req, res){
 });
 
 app.get("/logout", function(req, res){
     req.logout();
     res.redirect("/");
 });
 
 
 function isLoggedIn(req, res, next){
     if(req.isAuthenticated()){
         return next();
     }
     res.redirect("/login");
 }

app.listen(port, ()=> {
    console.log('Start Connection');
});
