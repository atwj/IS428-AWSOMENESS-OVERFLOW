import React, { Component } from 'react';
import {Sigma, NodeShapes,RelativeSize, EdgeShapes,SigmaEnableWebGL, LoadJSON} from 'react-sigma'


class Chart2 extends Component {
    constructor(props){
        super(props)
    }
    componentDidMount(){

    }
    componentDidUpdate(){

    }

    render(){
        return(
            <Sigma renderer="webgl" graph={{nodes:["id0", "id1"], edges:[{id:"e0",source:"id0",target:"id1"}]}}>
                <EdgeShapes default="dotted"/>
                <NodeShapes default="star"/>
                <RelativeSize initialSize={20}/>
            </Sigma>
        );
    }
}

export default Chart2;