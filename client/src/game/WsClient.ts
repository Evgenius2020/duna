import {GameState, Turn} from "./types";

export class WsClient {
    private readonly ws: WebSocket
    private readonly onBoardReceive;

    constructor(onGameStateReceive: (gameState: GameState) => void) {
        console.log('ws')
        this.onBoardReceive = onGameStateReceive;

        this.ws = new WebSocket('ws://localhost:8765');
        this.ws.addEventListener('open', () => {
            this.ws.addEventListener('message',
                (message) => {
                    this.onMessage(JSON.parse(message.data))
                });
            this.sendGetBoard();
        });
    }

    public sendGetBoard() {
        this.ws.send(JSON.stringify({type: 'GetGameState'}));
    }

    public sendTurn(turn: Turn) {
        this.ws.send(JSON.stringify({type: 'SendTurn', turn: turn}));
    }

    private onMessage(message: {
        type: string,
        gameState: GameState
    }) {
        if (message.type == 'SendGameState') {
            this.onBoardReceive(message.gameState);
        }
    }
}