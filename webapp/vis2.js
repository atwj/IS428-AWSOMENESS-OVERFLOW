var d3 = require('d3')
var db = require('dbhandle')

var q = d3.queue()
q.defer(db.query, a,b,c)