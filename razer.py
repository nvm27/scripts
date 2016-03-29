#!/bin/env python3

import argparse
import pyrazer
import sys

def set_freq(razer, mouse, profile, freq):
    print("[{}] Setting new scan frequency: {}Hz... ".format(mouse, freq), end="", flush=True)

    if freq in razer.getSupportedFreqs(mouse):
        if razer.setFrequency(mouse, profile, freq) == 0:
            print("OK")
        else:
            print("ERROR")
    else:
        print("INVALID")

def set_res(razer, mouse, profile, res):
    print("[{}] Setting new scan resolution: {}dpi... ".format(mouse, res), end="", flush=True)

    if res in razer.getSupportedRes(mouse):
        mapping = razer.getDpiMapping(mouse, profile)

        result = True
        result = result and (razer.changeDpiMapping(mouse, mapping, 0, res) == 0)
        result = result and (razer.changeDpiMapping(mouse, mapping, 1, res) == 0)

        print("OK") if result else print("ERROR")
    else:
        print("INVALID")

def razer_it_all(args):
    razer = pyrazer.Razer()

    for mouse in razer.getMice():
        profile = razer.getActiveProfile(mouse)

        if args.set_frequency:
            set_freq(razer, mouse, profile, args.set_frequency)
        if args.set_resolution:
            set_res(razer, mouse, profile, args.set_resolution)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Configure basic properties of Razer mice."
    )

    parser.add_argument(
        "-f", "--set-frequency",
        metavar="FREQUENCY",
        help="Set scan frequency in Hz",
        type=int
    )
    parser.add_argument(
        "-r", "--set-resolution",
        metavar="RESOLUTION",
        help="Set scan resolution in DPI",
        type=int
    )

    args = parser.parse_args()

    if len(sys.argv) > 1:
        razer_it_all(args)
