import {FC, useMemo} from "react";
import {GameStatusProps, TurnStatus} from "../types";

const GameStatus: FC<
    {
        gameStatusProps: GameStatusProps
    }> = ({gameStatusProps}) => {

    const turnStatusText = useMemo(() => {
        if (gameStatusProps.turnStatus == TurnStatus.White) {
            return 'Ход белых'
        } else {
            return 'Ход черных'
        }
    }, [gameStatusProps]);

    return (
        <div className='game-status'>
            <span className='score-text'>
                {turnStatusText}
            </span>

            <div className='meh'>
                <div className='score-text'>
                    <div className='piece black'/>
                    <span>{gameStatusProps.blackLosses}</span>
                </div>

                <div className='score-text'>
                    <div className='piece white'/>
                    <span>{gameStatusProps.whiteLosses}</span>
                </div>
            </div>
        </div>);
}

export default GameStatus;