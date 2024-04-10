import React from 'react'
import ReactDOM from 'react-dom/client'
import { NextUIProvider } from '@nextui-org/react'
import { RouterProvider, createHashRouter } from 'react-router-dom'
import './index.css'

import WebApp from '@twa-dev/sdk'
import HomePage from './pages/HomePage.tsx'

const router = createHashRouter([
  {
    path: '/',
    element: <HomePage />,
  }
]);

WebApp.ready();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <NextUIProvider>
      <RouterProvider router={router} />
    </NextUIProvider>
  </React.StrictMode>,
)
