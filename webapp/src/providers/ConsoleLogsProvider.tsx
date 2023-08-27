import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'

type consoleLogsType = Array<string> | undefined
type setConsoleLogsType = Dispatch<SetStateAction<consoleLogsType>>

interface IConsoleLogsProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface IConsoleLogsProviderContext {
  consoleLogs: consoleLogsType
  setConsoleLogs: setConsoleLogsType,
}

const ConsoleLogsProviderContext = createContext<IConsoleLogsProviderContext>({
  consoleLogs: [],
  setConsoleLogs: () => undefined,
});

export default function ConsoleLogsProvider({ children }: IConsoleLogsProviderProps) {
  const [consoleLogs, setConsoleLogs] = useState<consoleLogsType>([])

  return (
    <ConsoleLogsProviderContext.Provider
      value={{
        consoleLogs,
        setConsoleLogs,
      }}
    >
      {children}
    </ConsoleLogsProviderContext.Provider>
  )
}

export function useConsoleLogs(): [consoleLogsType, setConsoleLogsType] {
  const context = useContext(ConsoleLogsProviderContext)
  if (!context)
    throw new Error('useConsoleLogs must be used within a ConsoleLogsProvider')
  const { consoleLogs, setConsoleLogs } = context
  return [consoleLogs, setConsoleLogs]
}
