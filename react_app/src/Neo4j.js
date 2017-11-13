// import r from 'requests'
import axios from 'axios'

let config = {
    method: 'post',
    url: 'http://35.198.202.139:7474/db/data/',
    headers: {'X-Stream': true, 'Content-type': 'application/json; charset=utf-8', 'Accept':'application/json'}
}
export function cypher (query,params) {
    console.log('this runs')
    return axios({
        'method': config.method,
        'url': config.url,
        'headers': config.headers,
        'data':{
            'query':query,
            'params':params,
            'resultDataContents':['graph']
        }
        })
}


