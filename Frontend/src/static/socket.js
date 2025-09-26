import { io } from "socket.io-client";
const base = import.meta.env.VITE_API_BASE_URL;
const socket = io(base, {
  autoConnect: false,
  transports: ["websocket"], 
});


export default socket;
