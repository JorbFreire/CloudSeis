import { suParametersType } from "types/seismicUnixTypes";

export function getEmptyParams(name: string): suParametersType {
  switch (name) {
    case "sufilter":
      return {
        f: "",
        amps: "",
        dt: "",
      }

    case "suwind":
      return {
        key: "",
        min: "",
        max: "",
        verbose: "",
        abs: "",
        j: "",
        skip: "",
        count: "",
        reject: "",
        accept: "",
        ordered: "",
        dt: "",
        f1: "",
        tmin: "",
        tmax: "",
        itmin: "",
        itmax: "",
        nt: "",
      }

    case "sustack":
      return {
        key: "",
        normpow: "",
        repeat: "",
        nrepeat: "",
        verbose: "",
      }

    // "sugain"
    default:
      return {
        panel: "",
        tpow: "",
        epow: "",
        etpow: "",
        gpow: "",
        agc: "",
        gagc: "",
        wagc: "",
        trap: "",
        clip: "",
        pclip: "",
        nclip: "",
        qclip: "",
        qbal: "",
        pbal: "",
        mbal: "",
        maxbal: "",
        scale: "",
        norm: "",
        bias: "",
        jon: "",
        verbose: "",
        mark: "",
        vred: "",
      }
  }
}
