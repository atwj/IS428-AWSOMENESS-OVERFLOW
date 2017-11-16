var axios = require('axios')

/*
* Usage
*
* required arguments: statements, an array of statement of the following object
* {
*   statement: 'MATCH (n:User{ID: $id})-[:TYPE]-(a) return *',
*   parameters : {'id': 'Amos'},
*   resultDataContents: ['graph,'row'] // Either one or both
* }
* optional: transform: Series of functions to apply on the data before being passed to the resulting then() or catch()
* method.
* */
var query = function(statements, transform){
    var config = {
        headers:{'Content-type':'json','Accept':'application/json; charset=utf-8', 'X-stream':true},
        data: {
            "statements":statements
        }
    }
    if (typeof transform !== 'undefined') {
        config.transformResponse = transform
    }
    // returns promise
    return axios.post('http://35.198.202.139:7474/db/data/transaction/commit', config)
}

module.exports = {
    query: query
}

