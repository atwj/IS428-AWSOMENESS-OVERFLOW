const express = require('express')
const app = express();
const path = require('path')
const router = express.Router()

//static paths
app.use(express.static('./public'))
app.use('/', router)

// Vis paths
router.get('/', (req, res) => res.send('This is home'))
router.get('/vis1', (req, res) => res.sendFile('public/www/index.html',{root:__dirname}))
router.get('/vis2', (req, res) => res.sendFile('public/www/vis2.html',{root:__dirname}))
router.get('/vis3', (req, res) => res.sendFile('public/www/vis3.html',{root:__dirname}))
router.get('/vis4', (req, res) => res.sendFile('public/www/btwnness.html',{root:__dirname}))

app.listen(3000, () => console.log('App listening at localhost:3000'))