import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'
import { SnackbarProvider } from 'notistack'

import NotificationManager from 'components/NotificationsManager'
import './index.css'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <SnackbarProvider maxSnack={10}>
      <NotificationManager>
        <Routes />
      </NotificationManager>
    </SnackbarProvider>
  </React.StrictMode >
)
