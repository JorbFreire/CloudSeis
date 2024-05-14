import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'

import ConsoleLogsProvider from 'providers/ConsoleLogsProvider'
import LinesProvider from 'providers/LinesProvider'
import SelectedCommandProvider from 'providers/SelectedCommandProvider'
import './index.css'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ConsoleLogsProvider>
      <LinesProvider>
        <SelectedCommandProvider>
          <Routes />
        </SelectedCommandProvider>
      </LinesProvider>
    </ConsoleLogsProvider>
  </React.StrictMode>
)
