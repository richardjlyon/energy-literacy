"""Visualise EROEI and net energy. See: http://euanmearns.com/eroei-for-beginners/"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
import copy

from energy_literacy import PLOT_DIR


def net_from_eroei(eroei: float) -> float:
    """Convert EROEI to net energy.

    # https://www.resilience.org/stories/2011-11-26/energy-return-investment-threshold/
    # net = out - in
    # EROEI = out / in

    Args:
        eroei: Energy return over energy in.

    Returns:
        Net energy as a percent.

    """

    return (eroei - 1) / eroei


def main():

    eroeis = np.arange(30, 1, -0.01)
    society = [net_from_eroei(eroei) for eroei in eroeis]
    energy_system = [1 - x for x in society]
    equivalent = [1 / s for s in society]

    df = pd.DataFrame(
        data={"society": society, "system": energy_system, "equivalent": equivalent},
        index=eroeis,
    )

    fig, (ax1, ax2) = plt.subplots(
        ncols=1, nrows=2, figsize=(10, 10 * 9 / 16), sharex=True
    )

    rect = matplotlib.patches.Rectangle(
        (1, 0), 6, 1.0, linewidth=1, edgecolor="red", facecolor="tab:red", alpha=0.1,
    )

    df["society"].plot(ax=ax1, label="Energy available to society", color="tab:green")

    # Upper: Net energy

    ax1.set_title("'Renewables' are forcing net energy off a cliff...", loc="left")
    ax1.set_ylabel("Available Energy / All Energy")
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, 0))

    ax1.fill_between(df.index, df["society"], color="tab:green", alpha=0.1)
    df["system"].plot(
        ax=ax1, label="Energy required to obtain energy", color="tab:red",
    )
    ax1.fill_between(df.index, df["system"], color="tab:red", alpha=0.1)

    ax1.annotate(
        "hydrocarbons",
        (25, net_from_eroei(25)),
        (25, 0.3),
        xycoords="data",
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1, ls="--"),
    )

    RENEWABLES_EROEI = 7
    ax1.annotate(
        "'renewables'",
        (RENEWABLES_EROEI, net_from_eroei(RENEWABLES_EROEI)),
        (13, 0.3),
        xycoords="data",
        arrowprops=dict(arrowstyle="-|>", color="black", lw=1, ls="--"),
    )

    ax1.add_patch(rect)

    ax1.legend(loc="upper center")

    # Lower: equivalent energy system

    ax2.set_title(
        "'Renewables' require multiples of current generating capacity to maintain available energy...",
        loc="left",
    )
    ax2.set_ylabel("Multiple of current system")
    ax2.set_xlabel("Energy Returned / Energy In")

    rect = matplotlib.patches.Rectangle(
        (1, 0), 6, 5.0, linewidth=1, edgecolor="red", facecolor="tab:red", alpha=0.1,
    )
    ax2.add_patch(rect)
    ax2.set_ylim(0, 5)

    df["equivalent"].plot(
        ax=ax2, label="Energy required to obtain energy", color="tab:blue",
    )

    ax2.annotate(
        "CIVILISATION\nCOLLAPSE",
        (0, 0),
        (610, 150),
        color="tab:red",
        xycoords="axes points",
        textcoords="offset pixels",
    )

    ax2.annotate(
        "?? Lyon Energy Futures Ltd. (2022)",
        (0, 0),
        (20, 30),
        xycoords="figure points",
        textcoords="offset pixels",
        va="top",
        color="grey",
    )

    plt.gca().invert_xaxis()

    outfile = PLOT_DIR / f"renewables_forcing_energy_off_a_cliff.png"
    plt.savefig(outfile)
    print(f"\nSaved file to {outfile}")

    plt.show()


if __name__ == "__main__":
    main()
