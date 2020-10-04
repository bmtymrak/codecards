import React, { useState } from 'react';
import Card from './Card.js';
// import './App.css';

function App({ setup, socket }) {

    const [activeTeam, setActiveTeam] = useState(setup[1])
    const [cards, setCards] = useState(setup[0])
    const [remainingCards, setRemainingCards] = useState(updateScore(setup[0]))
    const [callerView, setCallerView] = useState(false)
    const [canClick, setCanClick] = useState(true)
    const [gameActive, setGameActive] = useState(true)

    socket.onmessage = (e) => {
        const data = JSON.parse(e.data)
        if (data["event_type"] == "card click") {
            let card = data['card']
            onTouch(card)
        } else if (data["event_type"] == "end turn") {
            handleCanClick()
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

    function onTouch(card) {
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

    function handleEndOfGame() {
        setGameActive(false)
        const newActiveTeam = activeTeam === 'blue' ? 'red' : 'blue'
        setActiveTeam(newActiveTeam)
        setCallerView(true)
    }

    function handleViewChange() {
        setCallerView(prevCallerView => !callerView)
    }

    function endTurn() {
        socket.send(JSON.stringify({
            'event_type': 'end turn'
        }))
    }

    function handleCanClick() {
        if (gameActive) {
            const newActiveTeam = activeTeam === 'blue' ? 'red' : 'blue'
            setActiveTeam(newActiveTeam)
            setCanClick(true)
        }
    }

    function newGame() {
        // let [cards, firstTeam] = createBoard()
        // setCards(cards)
        // setActiveTeam(firstTeam)
        // setRemainingCards(updateScore(cards))
        // setCanClick(true)
        // setGameActive(true)
        // setCallerView(false)
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
                <button onClick={newGame}>
                    New Game
          </button>
            </div>
            <div className="board-container">
                {cards.map((card) => (
                    <Card
                        key={card.word}
                        card={card}
                        activeTeam={activeTeam}
                        onTouch={onTouch}
                        callerView={callerView}
                        canClick={canClick}
                        socket={socket}
                        colors={{ 'red': '#ea4f4f', 'blue': '#338bea', 'assassin': 'gray', 'none': '#979777' }}
                        colorsCaller={{ 'red': '#eebaba', 'blue': 'rgb(130, 188, 244)', 'assassin': '#c4c4c4' }}
                    />))}
            </div>
        </div>
    )
}

export default App;