import React from 'react';
import ReactDOM from "react-dom";
import App from './App.js'


const cards = JSON.parse(document.getElementById("cards").textContent)
console.log(cards)

function countCards(cards) {
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


const initialCards = countCards(cards)
const firstTeam = initialCards["red"] > initialCards["blue"] ? "red" : "blue"
const setup = [cards, firstTeam]

const gameID = JSON.parse(document.getElementById("game").textContent)

let ws_protocol = 'ws://'
if (window.location.protocol === "https:") {
    ws_protocol = 'wss://'
}

const socket = new WebSocket(ws_protocol + window.location.host + '/ws/games' + gameID)

ReactDOM.render(
    <React.StrictMode>
        <App setup={setup} socket={socket} />
    </React.StrictMode>,
    document.getElementById('root')
);