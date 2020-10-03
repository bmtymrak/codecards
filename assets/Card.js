import React, { useState } from 'react';
// import './Card.css';

function Card(props) {

    const [bgColor, setBgColor] = useState('beige')
    const [textColor, setTextColor] = useState('black')

    let style = {
        backgroundColor: bgColor,
        color: textColor,
    }

    if (props.callerView) {
        if (props.card.team !== 'none' & !props.card.clicked & bgColor !== props.colorsCaller[props.card.team]) {
            setBgColor(props.colorsCaller[props.card.team])
        }
    } else {
        if (props.card.clicked & bgColor !== props.colors[props.card.team]) {
            setBgColor(props.colors[props.card.team])
            setTextColor('white')
        }
        else if (!props.card.clicked & bgColor !== 'beige') {
            setBgColor('beige')
        }
    }

    const showCardColor = event => {
        if (!props.card.clicked && !props.callerView && props.canClick) {
            props.socket.send(JSON.stringify({
                'event_type': 'card click',
                'card': props.card
            }))
        }
    }

    return (
        <div className="card" onClick={showCardColor} style={style}>{props.card.word.toUpperCase()}</div>
    )
}

export default Card