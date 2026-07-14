const CLIENT_ID_KEY = 'teumSeoulClientId'

export function useClientId() {
  let clientId = localStorage.getItem(CLIENT_ID_KEY)
  if (!clientId) {
    clientId = crypto.randomUUID()
    localStorage.setItem(CLIENT_ID_KEY, clientId)
  }
  return clientId
}
