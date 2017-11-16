var axios = require('axios')

// Retrieve graph for given tag for relationships of type: comments, answers, parent_of and last_edit
var query = function(statements, params, output, transform){
    var config = {
        headers:{'Content-type':'json','Accept':'application/json; charset=utf-8', 'X-stream':true},
        data: {
            "statements":statements,
            "parameters": params,
            "resultDataContents":output
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

