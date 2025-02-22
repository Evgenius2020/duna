import {FC, useMemo} from "react";
import {GameStatusProps} from "../types";

const GameStatus: FC<
    {
        gameStatusProps: GameStatusProps
    }> = ({gameStatusProps}) => {

    const turnStatusText = useMemo(() => {
        if (gameStatusProps.side === gameStatusProps.turnStatus) {
            return 'Ваш ход'
        } else {
            return 'Ход оппонента'
        }
    }, [gameStatusProps]);

    return (
        <div className='game-status'>
            <span className='score-text'>
                {turnStatusText}
            </span>

            <div>
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