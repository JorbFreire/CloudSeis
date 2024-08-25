import { cleanup } from '@testing-library/react'

import { renderHook } from '@testing-library/react-hooks'
import { useLogsStore } from "./logsStore"

describe("Logs Store", () => {
  afterEach(cleanup)
  it("Should be empty Map", () => {
    const { result } = renderHook(() => useLogsStore())

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs).toEqual(new Map())
    expect(result.current.logs.size).toBe(0)
  })

  it("Should push new log", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(0, "log message")

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(0)).toEqual(["log message"])
  })

  it("Should push new log at non initialized position", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(37, "log message")

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(37)).toEqual(["log message"])
  })

  it("Should push multiple new logs", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(3, "log message 1")
    result.current.pushNewLog(3, "log message 2")
    result.current.pushNewLog(3, "log message 3")
    result.current.pushNewLog(3, "log message 4")

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(3)).toEqual([
      "log message 1",
      "log message 2",
      "log message 3",
      "log message 4",
    ])
  })

  it("Should push new logs to multiple keys", () => {
    const { result } = renderHook(() => useLogsStore())
    result.current.pushNewLog(7, "log message 1")
    result.current.pushNewLog(7, "log message 2")

    result.current.pushNewLog(9, "log message 1")
    result.current.pushNewLog(9, "log message 2")

    result.current.pushNewLog(2, "log message 1")
    result.current.pushNewLog(2, "log message 2")

    expect(result.current.logs).toBeInstanceOf(Map)
    expect(result.current.logs.get(7)).toEqual([
      "log message 1",
      "log message 2",
    ])
    expect(result.current.logs.get(9)).toEqual([
      "log message 1",
      "log message 2",
    ])
    expect(result.current.logs.get(2)).toEqual([
      "log message 1",
      "log message 2",
    ])
  })
})
