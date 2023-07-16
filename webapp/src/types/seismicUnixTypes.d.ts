import { PositiveInteger } from 'newtype-ts/lib/PositiveInteger'
import { Positive as PositiveFloat } from 'newtype-ts/lib/Positive'

// !booleans in seismicunix probably be literaly the numbers 0 ou 1
type suFileHeader = | "tracl" | "tracr" | "fldr" | "tracf" | "ep" | "cdp" | "cdpt" | "trid" | "nvs" | "nhs" | "duse" | "offset" | "gelev" | "selev" | "sdepth" | "gdel" | "sdel" | "swdep" | "gwdep" | "scalel" | "scalco" | "sx" | "sy" | "gx" | "gy" | "counit" | "wevel" | "swevel" | "sut" | "gut" | "sstat" | "gstat" | "tstat" | "laga" | "lagb" | "delrt" | "muts" | "mute" | "ns" | "dt" | "gain" | "igc" | "igi" | "corr" | "sfs" | "sfe" | "slen" | "styp" | "stas" | "stae" | "tatyp" | "afilf" | "afils" | "nofilf" | "nofils" | "lcf" | "hcf" | "lcs" | "hcs" | "year" | "day" | "hour" | "minute" | "sec" | "timbas" | "trwf" | "grnors" | "grnofr" | "grnlof" | "gaps" | "otrav" | "d1" | "f1" | "d2" | "f2" | "ungpow" | "unscale"

declare type sufilterComandType = {
  name: "sufilter"
  parameters: {
    f: Array<PositiveFloat>,
    amps: Array<PositiveFloat>,
    dt: Array<PositiveFloat>,
  }
}

declare type suwindComandType = {
  name: "suwind"
  parameters: {
    // * propably required, but not required on CLI
    key: suFileHeader,
    min: PositiveInteger,
    max: PositiveInteger,

    // * not required at all
    verbose: boolean,
    abs: boolean,
    j: PositiveInteger,
    skip: PositiveInteger,
    count: PositiveInteger,
    // ?"reject" and "accept" are bad typed?
    reject: Array<PositiveFloat>,
    accept: Array<PositiveFloat>,
    // ? *** //
    ordered: 0 | 1 | -1,
    dt: PositiveFloat,
    f1: PositiveFloat,
    tmin: PositiveFloat,
    tmax: PositiveFloat,
    itmin: PositiveInteger,
    itmax: PositiveInteger,
    nt: PositiveInteger,
  }
}

declare type sustackComandType = {
  name: "sustack"
  parameters: {
    key: suFileHeader,
    normpow: PositiveFloat,
    repeat: boolean,
    nrepeat: PositiveInteger,
    verbose: boolean,
  }
}

declare type sugainComandType = {
  name: "sugain"
  parameters: {
    panel: boolean,
    tpow: PositiveFloat,
    epow: PositiveFloat,
    etpow: PositiveFloat,
    gpow: PositiveFloat,
    agc: boolean,
    gagc: boolean,
    wagc: PositiveFloat,
    trap: PositiveFloat,
    clip: PositiveFloat,
    pclip: PositiveFloat,
    nclip: PositiveFloat,
    qclip: PositiveFloat,
    qbal: boolean,
    pbal: boolean,
    mbal: boolean,
    maxbal: boolean,
    scale: PositiveFloat,
    norm: PositiveFloat,
    bias: PositiveFloat,
    jon: boolean,
    verbose: boolean,
    mark: boolean
    vred: PositiveFloat
  }
}

declare type suCommandsQueue = Array<
  sufilterComandType |
  suwindComandType |
  sustackComandType |
  sugainComandType
>
