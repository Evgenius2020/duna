import React from 'react';
import Board from "./board/board";

class App extends React.Component {
    render() {
        return (
            <Board onTurnAttempt={console.log}/>
        );
    }
}

export default App;
