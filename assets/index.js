import React from 'react';
import ReactDOM from "react-dom";
import App from './App.js'


const cards = JSON.parse(document.getElementById("cards").textContent)
const firstTeam = JSON.parse(document.getElementById("active_team").textContent)
const gameID = JSON.parse(document.getElementById("game").textContent)

const setup = [cards, firstTeam]

let ws_protocol = 'ws://'
if (window.location.protocol === "https:") {
    ws_protocol = 'wss://'
}

const socket = new WebSocket(ws_protocol + window.location.host + '/ws/games' + gameID)

ReactDOM.render(
    <React.StrictMode>
        <App setup={setup} socket={socket} gameID={gameID} />
    </React.StrictMode>,
    document.getElementById('root')
);