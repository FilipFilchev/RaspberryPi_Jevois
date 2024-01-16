//npm install socket.io-client

import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const SOCKET_SERVER_URL = "http://localhost:5000";

const App = () => {
    const [missionStatus, setMissionStatus] = useState('');

    useEffect(() => {
        const socket = io(SOCKET_SERVER_URL);

        socket.on('mission_status', (message) => {
            console.log(message);
            setMissionStatus(message);
        });

        return () => socket.disconnect();
    }, []);

    const startDroneMission = () => {
        const socket = io(SOCKET_SERVER_URL);
        socket.emit('start_mission');
    };

    return (
        <div>
            <button onClick={startDroneMission}>Start Drone Mission</button>
            <p>Mission Status: {missionStatus}</p>
        </div>
    );
};

export default App;
