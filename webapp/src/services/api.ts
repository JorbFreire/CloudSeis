import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

export default api