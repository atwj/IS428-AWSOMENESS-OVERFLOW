import React, { Component } from 'react';
import './App.css';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Grid from 'material-ui/Grid'
// import {Sigma, RandomizeNodePositions, RelativeSize} from 'react-sigma';
// import {cypher} from './Neo4j.js'

const styles = theme => ({
    root: {
        marginTop: theme.spacing.unit * 3,
        width: '100%',
    },
});

class NetworkGraph extends Component {
    
}

class TopAppBar extends Component {
    constructor(props){
        super(props)
        this.classes = props
    }
    render(){
        return (
                <AppBar position="static" color="default">
                    <Toolbar>
                        <Typography type="title" color="inherit">
                            Awesomeness Overflow
                        </Typography>
                    </Toolbar>
                </AppBar>
        );
    }
}

class Clock extends Component{
    constructor(props){
        super(props)
        this.state = {date:new Date()}
    }

    componentDidMount () {
        this.timerID = setInterval(() => this.tick(), 1000)
    }

    componentWillUnmount () {
        clearInterval(this.timerID)
    }

    tick() {
        this.setState({date: new Date()});
    }

    render() {
        return (
        <div>
            <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
        </div>
        )
    }
}

class App extends Component {
  render() {
    return (
        <div>
            <TopAppBar/>
            <div>div1</div>
            <div>div2</div>
            <div>div3</div>
        </div>

    );
  }
}

export default App;

/*
<div className="App">
    <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Welcome to React</h1>
        <p>Hello my name is Amos!</p>
    </header>
    <Clock/>
    <p className="App-intro">
        To get started, edit <code>src/App.js</code> and save to reload.
    </p>
</div>
*/