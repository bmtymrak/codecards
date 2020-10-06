import React, { useState } from 'react';
import Card from './Card.js';

function App({ setup, socket, gameID }) {

    const [activeTeam, setActiveTeam] = useState(setup[1])
    const [cards, setCards] = useState(setup[0])
    const [remainingCards, setRemainingCards] = useState(updateScore(setup[0]))
    const [callerView, setCallerView] = useState(false)
    const [canClick, setCanClick] = useState(true)
    const [gameActive, setGameActive] = useState(true)

    socket.onmessage = (e) => {
        const data = JSON.parse(e.data)
        if (data["event_type"] === "card click") {
            let card = data['card']
            onCardClick(card)
        } else if (data["event_type"] === "end turn") {
            handleChangeTeam(data['active_team'])
        } else if (data["event_type"] === "new_game") {
            startNewGame(data['cards'])
        }

    }

    function updateScore(cards) {
        return (cards.reduce((teamRemaining, card) => {
            if (card.clicked === false) {
                if (card.team in teamRemaining) {
                    teamRemaining[card.team]++
                } else {
                    teamRemaining[card.team] = 1
                }
            }
            return teamRemaining
        }, {})
        )
    }

    function handleCardClick(card) {
        if (!card.clicked && !callerView && canClick) {
            socket.send(JSON.stringify({
                'event_type': 'card click',
                'card': card,
            }))
        }
    }


    function onCardClick(card) {
        const newCards = [...cards]
        const index = newCards.findIndex(compCard => compCard.word == card.word)
        newCards[index].clicked = true
        setCards(newCards)
        const score = updateScore(newCards)
        setRemainingCards(score)

        if (!score[activeTeam]) {
            setGameActive(false)
            setCanClick(false)
            setCallerView(true)
        }

        else if (activeTeam !== card.team) {
            setCanClick(false)
        }

        if (card.team === 'assassin') {
            handleEndOfGame()
        }

    }

    function handleViewChange() {
        setCallerView(prevCallerView => !callerView)
    }

    function endTurn() {
        socket.send(JSON.stringify({
            'event_type': 'end turn'
        }))
    }

    function handleEndOfGame() {
        setGameActive(false)
        const newActiveTeam = activeTeam === 'blue' ? 'red' : 'blue'
        setActiveTeam(newActiveTeam)
        setCallerView(true)
    }


    function handleChangeTeam(newActiveTeam) {
        if (gameActive) {
            // const newActiveTeam = activeTeam === 'blue' ? 'red' : 'blue'
            setActiveTeam(newActiveTeam)
            setCanClick(true)
        }
    }

    function handleNewGame() {
        socket.send(JSON.stringify({
            'event_type': 'new game',
            'game_id': gameID,
        }))
    }

    function startNewGame(newCards) {
        setCards(newCards)
        const newScore = updateScore(newCards)
        setRemainingCards(newScore)
        setActiveTeam(newScore["red"] > newScore["blue"] ? "red" : "blue")
        setCanClick(true)
        setGameActive(true)
        setCallerView(false)
    }

    return (
        <div className="container">
            <h1>{gameActive ? `${activeTeam.slice(0, 1).toUpperCase() + activeTeam.slice(1)}'s turn` : `${activeTeam.slice(0, 1).toUpperCase() + activeTeam.slice(1)} wins!`}</h1>
            <div className="score-container">
                <div className="score blue">{remainingCards.blue ? remainingCards.blue : 0}</div>
                <button onClick={endTurn}>
                    {activeTeam === 'blue' ? 'End Blue turn' : 'End Red turn'}
                </button>
                <div className="score red">{remainingCards.red ? remainingCards.red : 0}</div>
            </div>
            <div className="controls-container">
                <button onClick={handleViewChange}>
                    {callerView ? 'Switch to Player View' : 'Switch to Caller View'}
                </button>
                <button onClick={handleNewGame}>
                    New Game
          </button>
            </div>
            <div className="board-container">
                {cards.map((card) => (
                    <Card
                        key={card.word}
                        card={card}
                        activeTeam={activeTeam}
                        handleCardClick={handleCardClick}
                        callerView={callerView}
                        canClick={canClick}
                        socket={socket}
                        textColor={card.clicked === true ? 'white' : 'black'}
                        colors={{ 'red': '#ea4f4f', 'blue': '#338bea', 'assassin': 'gray', 'none': '#979777' }}
                        colorsCaller={{ 'red': '#eebaba', 'blue': 'rgb(130, 188, 244)', 'assassin': '#c4c4c4' }}
                    />))}
            </div>
        </div>
    )
}

export default App;