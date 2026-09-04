"""Versao de terminal do E7 AutoBuy (usa o nucleo e7core).

Pergunta quantos SKYSTONES gastar (cada refresh custa 3) e roda ate
atingir a meta. Para a qualquer momento com CTRL+C. A interface grafica
fica em autobuy_gui.py.
"""
import sys
import datetime
import ctypes
from tkinter import Tk, simpledialog

from e7core import E7Core, log_crash, SKYSTONES_PER_REFRESH


def msg(text, title="E7 AutoBuy", flags=0):
    return ctypes.windll.user32.MessageBoxW(0, text, title, flags)


def main():
    Tk().withdraw()
    core = E7Core()

    try:
        core.setup()
    except Exception:
        log_crash("\nCheck your config.ini / ADB")
        msg("Algo deu errado ao iniciar. Veja crash.log")
        sys.exit()

    sky = simpledialog.askinteger(
        " ", "Quantos SKYSTONES quer gastar?\n(cada refresh custa 3)")
    if not sky:
        sys.exit()
    rolls = sky // SKYSTONES_PER_REFRESH
    if rolls < 1:
        msg("Informe pelo menos 3 skystones (1 refresh).")
        sys.exit()

    try:
        print(f"Device: {core.device}")
        print(f"Display do E7: fisico={core.e7_display} logico={core.e7_input_display}")
        print("TO STOP ANYTIME PRESS CTRL+C IN THE CONSOLE")
        resolution = core.screen()
    except Exception:
        log_crash("\nADB isn't working")
        msg("ADB nao esta funcionando. Veja crash.log")
        sys.exit()

    if not core.is_16_9(resolution):
        msg(f"Resolution {resolution.size[0]}x{resolution.size[1]} not supported, "
            "use 16:9 aspect ratio", "Error")
        sys.exit()
    core.compute_coords(resolution)

    real_sky = rolls * SKYSTONES_PER_REFRESH
    et = str(datetime.timedelta(seconds=(rolls * 11.5 * core.delay)))[:8]
    if msg(f"Skystones = {real_sky}\nRefreshes = {rolls}\nDelay = {core.delay}x\n"
           f"Estimated time = {et}\nTO STOP ANYTIME PRESS CTRL+C\nReady to start ?",
           "Setup", 4) != 6:
        sys.exit()

    cBM = MM = 0
    start = datetime.datetime.now()
    completed = 0
    try:
        for x in range(rolls + 1):
            print(f"{x}/{rolls}")
            bm, mm = core.scan_and_buy()
            cBM += bm
            MM += mm
            completed = x
            if x == rolls:
                break
            core.reroll()
    except KeyboardInterrupt:
        pass
    except Exception:
        log_crash()
        msg("Something went wrong, check crash.log file", "Crash Handler")
        sys.exit()

    end = datetime.datetime.now()
    gold = ((184 * cBM) + (280 * MM)) * 1000
    results = (f"Covenant Bookmark = {5 * cBM}\nMystic Medals = {50 * MM}\n"
               f"Gold Spent = {gold}\n")
    with open("logs.txt", "a") as log:
        log.write(f"Started at {start}\nEnded at {end}\n"
                  f"Time elapsed: {end - start}\nRefreshes = {completed}\n"
                  f"Skystones spent = {completed * SKYSTONES_PER_REFRESH}\n{results}\n")
    msg(results, "Results")


if __name__ == "__main__":
    main()
