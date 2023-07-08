
import React from 'react';

export default function App(){
   return(
      <button onClick={()=>{
         ipcRenderer.send('async-test', 'ping')
         // reply
         ipcRenderer.on('asynchronous-reply', (event, arg) => {
         console.log("Hiii",arg) // prints "Hiii pong"
         })
     }}>Async</button>
  )

}