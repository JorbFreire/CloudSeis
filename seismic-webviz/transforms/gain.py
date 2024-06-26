import sys
from math import isclose, sqrt, exp

import numpy as np
import numpy.typing as npt

EPS: float = 3.8090232  # exp(-EPS*EPS) = 5e-7, "noise" level


def err(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)
    sys.exit(1)


def warn(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


def gain(
    data: npt.NDArray,
    tpow: float,
    epow: float,
    etpow: float,
    gpow: float,
    vred: float,
    agc: bool,
    gagc: bool,
    qbal: bool,
    pbal: bool,
    mbal: bool,
    scale: float,
    bias: float,
    trap: float,
    clip: float,
    qclip: float,
    iwagc: float,
    tmin: float,
    dt: float,
    nt: int,
    maxbal: bool,
    pclip: float,
    nclip: float,
) -> npt.NDArray:
    f_two: float = 2.0
    f_one: float = 1.0
    f_half: float = 0.5

    if bias:
        print("RUN bias")
        data += bias
    if tpow:
        do_tpow(data, tpow, vred, tmin, dt, nt)
    if epow:
        do_epow(data, epow, etpow, tmin, dt, nt)
    if not isclose(gpow, f_one):
        print("RUN — !CLOSETO(gpow, f_one)")
        if isclose(gpow, f_half):
            err("not yet implemented")
        elif isclose(gpow, f_two):
            err("not yet implemented")
        else:
            err("not yet implemented")
    if agc:
        data = do_agc(data, iwagc, nt)
    if gagc:
        data = do_gagc(data, iwagc, nt)
    if trap > 0.0:
        data = do_trap(data, trap, nt)
    if clip > 0.0:
        data = do_clip(data, clip, nt)
    # if pclip < FLT_MAX:
    #     err("do_pclip() not yet implemented")
    # if nclip > -FLT_MAX:
    #     err("do_nclip() not yet implemented")
    if qclip < 1.0 and (not qbal):
        do_qclip(data, qclip, nt)
    if qbal:
        do_qbal(data, qclip, nt)
    if pbal:
        err("handling pbal True not yet implemented")
    if mbal:
        err("handling mbal True not yet implemented")
    if maxbal:
        err("handling maxbal True not yet implemented")
    if not isclose(scale, f_one):
        print("RUN — !CLOSETO(scale, f_one)")
        data *= scale

    return data


def do_tpow(data, tpow, vred, tmin, dt, nt):
    # TODO
    err("do_tpow() not yet implemented")


def do_epow():
    # TODO
    err("do_epow() not yet implemented")


def do_agc(data: npt.NDArray, iwagc: int, nt: int) -> npt.NDArray:

    # allocate room for agc'd data and square of data
    agcdata = np.zeros(nt, dtype=float)
    d2 = np.zeros(nt)

    # Compute square of data
    d2 = data * data

    # Initialize first half window and gain first sample
    _sum: float = 0.0
    for i in range(0, iwagc):
        _sum += d2[i]

    nwin: int = iwagc
    rms: float = _sum / nwin

    if rms == 0:
        agcdata[0] = 0
    else:
        agcdata[0] = data[i] / sqrt(rms)

    # ramping on : increase sum and nwin & gain data until reaching 2*iwagc-1 window
    # processing samples from 1 to iwagc-1
    for i in range(1, iwagc):
        _sum += d2[i + iwagc - 1]
        nwin += 1
        rms = _sum / nwin
        # rms = 0 implies data[i]=0
        if rms == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    # full 2*iagc rms window -- gain data
    # compute sum from 0 at each sample -- decreasing sum give inaccurate results, even negative RMS
    # processing samples from iwagc to nt-iwagc-1
    nwin += 1
    for i in range(iwagc, nt - iwagc):
        _sum = 0.0
        for j in range(i - iwagc, i + iwagc):
            _sum += d2[j]
        rms = _sum / nwin
        if rms == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    # ramping off -- decrease nwin -- gain data
    # compute sum from 0 at each sample -- decreasing sum give inaccurate results, even negative RMS
    # processing samples from nt-iwagc to nt-1
    for i in range(nt - iwagc, nt):
        _sum = 0
        for j in range(i - iwagc, nt):
            _sum += d2[j]
        nwin -= 1
        rms = _sum / nwin
        if data[i] == 0:
            agcdata[i] = 0
        else:
            agcdata[i] = data[i] / sqrt(rms)

    return agcdata


def do_gagc(data: npt.NDArray, iwagc: int, nt: int) -> npt.NDArray:
    agcdata: npt.NDArray  # agc'd data
    w: npt.NDArray  # Gaussian window weights
    d2: npt.NDArray  # square of input data
    s: npt.NDArray  # weighted sum of squarEPSes of the data
    u: float  # related to reciprocal std dev
    usq: float  # u*u

    # Allocate room for agc'd data
    agcdata = np.zeros(nt, dtype=float)

    # Allocate and compute Gaussian window weights
    w = np.zeros(iwagc, dtype=float)  # recall iwagc is HALF window
    u = EPS / iwagc
    usq = u * u

    for i in range(1, iwagc):
        floati = float(i)
        w[i] = exp(-(usq * floati * floati))

    # Allocate sum of squares and weighted sum of squares
    d2 = np.zeros(nt)
    s = np.zeros(nt)

    # Put sum of squares of data in d2 and
    # initialize s to d2 to get center point set
    for i in range(0, nt):
        val = data[i]
        s[i] = d2[i] = val * val

    # Compute weighted sum s; use symmetry of Gaussian
    for j in range(1, iwagc):
        wtmp = w[j]
        for i in range(j, nt):
            s[i] += wtmp * d2[i - j]
        k = nt - j
        for i in range(0, k):
            s[i] += wtmp * d2[i + j]

    for i in range(0, nt):
        stmp = s[i]
        agcdata[i] = 0.0 if (not stmp) else data[i] / sqrt(stmp)

    return agcdata


def do_trap(data, trap, nt):
    # TODO
    err("do_trap() not yet implemented")


def do_clip(data, clip, nt):
    # TODO
    err("do_clip() not yet implemented")


def do_pclip(data, pclip, nt):
    # TODO
    pass


def do_nclip(data, nclip, nt):
    # TODO
    err("do_nclip() not yet implemented")


def do_qclip(data, qclip, nt):
    # TODO
    pass


def do_qbal(data, qclip, nt):
    """Quantile balance"""
    # TODO
    err("do_qbal() not yet implemented")
