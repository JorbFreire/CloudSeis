import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'

import ConsoleLogsProvider from 'providers/ConsoleLogsProvider'
import SeismicUnixBlocks from 'providers/seismicUnixBlocks'
import SelectedCommandProvider from 'providers/SelectedCommandProvider'
import './index.css'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ConsoleLogsProvider>
      <SeismicUnixBlocks>
        <SelectedCommandProvider>
          <Routes />
        </SelectedCommandProvider>
      </SeismicUnixBlocks>
    </ConsoleLogsProvider>
  </React.StrictMode>
)
