import React from 'react'
import ReactDOM from 'react-dom/client'

import { Routes } from 'generouted/react-location'
import './index.css'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
      <Routes />
  </React.StrictMode>
)
