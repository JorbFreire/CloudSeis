import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'

import ConsoleLogsProvider from 'providers/ConsoleLogsProvider'
import SeismicUnixBlocks from 'providers/seismicUnixBlocks'
import './index.css'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ConsoleLogsProvider>
      <SeismicUnixBlocks>
        <Routes />
      </SeismicUnixBlocks>
    </ConsoleLogsProvider>
  </React.StrictMode>
)
