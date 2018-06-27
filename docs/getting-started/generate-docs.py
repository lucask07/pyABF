"""
Boilerplate use case scrpit.
"""

import os
import sys
sys.path.insert(0, "src/")  # for importing
sys.path.append("../../src/")  # for your IDE

import matplotlib.pyplot as plt
plt.style.use('bmh')
import numpy as np
import glob
import inspect


class Uses:
    def __init__(self):
        self.figsize = (8, 5)
        self.dpi = 75

    def saveAndClose(self):
        callingFunctionName = inspect.stack()[1][3]
        outputFolder = os.path.dirname(__file__)+"/source/"
        outputFile = os.path.abspath(outputFolder+callingFunctionName+".jpg")
        plt.savefig(outputFile, dpi=self.dpi)
        plt.close()

    def demo_01a_print_sweep_data(self):
        """
        ## Access Sweep Data

        Load an ABF and display data from a certain sweep. 
        """
        import pyabf
        abf = pyabf.ABF("data/abfs/17o05028_ic_steps.abf")
        abf.setSweep(14)  # sweeps start at 0
        print(abf.sweepY)  # sweep data (ADC)
        print(abf.sweepC)  # sweep command (DAC)
        print(abf.sweepX)  # sweep times (seconds)

    def demo_02a_plot_matplotlib_sweep(self):
        """
        ## Plot Sweep Data

        Plot a sweep of ABF data using matplotlib.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05028_ic_steps.abf")
        abf.setSweep(14)
        plt.figure(figsize=self.figsize)
        plt.plot(abf.sweepX, abf.sweepY, lw=.5)
        self.saveAndClose()

    def demo_03a_decorate_matplotlib_plot(self):
        """
        ## Decorate Plots with ABF Information

        Plot every 5th sweep and decorate the plot nicely.
        Note that the _displayed_ sweep number starts at 1.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05028_ic_steps.abf")

        plt.figure(figsize=self.figsize)
        for sweepNumber in range(abf.sweepCount)[::5]:
            abf.setSweep(sweepNumber)
            plt.plot(abf.sweepX, abf.sweepY, alpha=.5,
                     label=f"sweep {sweepNumber+1}")

        plt.margins(0, .1)
        plt.legend()
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.title(abf.abfID)
        plt.tight_layout()
        self.saveAndClose()

    def demo_04a_plotting_multiple_channels(self):
        """
        ## Plot Multi-Channel ABFs

        Channel selection is done by adding the `channel=` 
        argument in `setSweep()`
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/14o08011_ic_pair.abf")

        fig = plt.figure(figsize=self.figsize)

        abf.setSweep(sweepNumber=0, channel=0)
        ax1 = fig.add_subplot(211)
        ax1.set_title(f"Channel {abf.sweepChannel+1}")
        ax1.plot(abf.sweepX, abf.sweepY, lw=.5)
        ax1.set_ylabel(abf.sweepLabelY)

        abf.setSweep(sweepNumber=0, channel=1)
        ax2 = fig.add_subplot(212)
        ax2.set_title(f"Channel {abf.sweepChannel+1}")
        ax2.plot(abf.sweepX, abf.sweepY, lw=.5)
        ax2.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelY)

        fig.subplots_adjust(hspace=.4)  # add more space between the subplots

        self.saveAndClose()

    def demo_05a_plotting_command_waveform(self):
        """
        ## Plot the Stimulus Waveform

        Episodic ABF files can have complex protocols designed with the waveform
        editor. After calling `setSweep()` the command waveform can be accessed
        as `sweep.C`.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        abf.setSweep(14)

        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(211)
        ax1.set_title("ADC (recorded waveform)")
        ax1.plot(abf.sweepX, abf.sweepY, lw=.5)
        ax1.set_ylabel(abf.sweepLabelY)

        ax2 = fig.add_subplot(212)
        ax2.set_title("DAC (stimulus waveform)")
        ax2.plot(abf.sweepX, abf.sweepC, color='r')
        ax2.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelC)

        fig.subplots_adjust(hspace=.4)  # add more space between the subplots

        self.saveAndClose()

    def demo_06a_linking_subplots_and_zooming(self):
        """
        ## Zooming Gracefully

        While you can zoom in on data by setting its matplotlib axis, when
        using subplots it helps to link them together horizontally.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")
        abf.setSweep(14)

        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(211)
        ax1.set_title("ADC (recorded waveform)")
        ax1.plot(abf.sweepX, abf.sweepY, lw=.5)
        ax1.set_ylabel(abf.sweepLabelY)

        ax2 = fig.add_subplot(212, sharex=ax1)  # this links them together
        ax2.set_title("DAC (stimulus waveform)")
        ax2.plot(abf.sweepX, abf.sweepC, color='r')
        ax2.set_xlabel(abf.sweepLabelX)
        ax2.set_ylabel(abf.sweepLabelC)

        fig.subplots_adjust(hspace=.4)  # add more space between the subplots

        ax1.axes.set_xlim(0.1, 0.4)  # zoom between 100 and 200 ms

        self.saveAndClose()

    def demo_07a_stacked_sweeps(self):
        """
        ## Stacking Sweeps

        I often like to view sweeps stacked one on top of another. In ClampFit
        this is done with "distribute traces". Here we can add a bit of offset
        when plotting sweeps.

        Note also that `abf.sweepList` is the same as `range(abf.sweepCount)`
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/171116sh_0018.abf")

        plt.figure(figsize=self.figsize)

        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            plt.plot(abf.sweepX, abf.sweepY + 140*sweepNumber,
                     color='C0', lw=.5)

        plt.gca().get_yaxis().set_visible(False)  # hide Y axis
        plt.xlabel(abf.sweepLabelX)
        plt.margins(0, .02)
        plt.tight_layout()

        self.saveAndClose()

    def demo_08a_xy_offset(self):
        """
        ## XY Offset and Custom Colormap

        Plotting every sweep with a slight X and Y offset produces a cool
        3D effect. I often use this view to visually inspect drug effects.

        I also assign a color by sweep from a matplotlib colormap.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")

        # only plot data between this time range
        i1 = int(abf.dataRate*3.0)
        i2 = int(abf.dataRate*3.5)

        # use a custom colormap
        cm = plt.get_cmap("winter")
        colors = [cm(x/abf.sweepCount) for x in abf.sweepList]

        plt.figure(figsize=self.figsize)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            plt.plot(
                abf.sweepX[i1:i2] + .05 * sweepNumber,
                abf.sweepY[i1:i2] + 15*sweepNumber,
                color=colors[sweepNumber],
                lw=.5, alpha=.6)

        # remove axes and use tight margins
        plt.gca().get_yaxis().set_visible(False)  # hide Y axis
        plt.gca().get_xaxis().set_visible(False)  # hide X axis
        plt.margins(.02, .02)
        plt.tight_layout()

        self.saveAndClose()

    def demo_08b_using_plot_module(self):
        """
        ## Advanced Plotting with the `pyabf.plot` Module

        pyabf has a plot module which has been designed to simplify the act
        of creating matplotlib plots of electrophysiological data loaded with
        the ABF class. This module isn't fully developed yet (so don't rely
        on code you write today working with it tomorrow), but it's a strong
        start and has some interesting functionality that might be worth
        inspecting. 

        If you care a lot about how your graphs look, plot them yourself with
        matplotlib commands. If you want to save keystrokes, don't care how
        the graphs look, or don't know how to use matplotlib (and don't feel
        like learning), maybe some of the functions in `pyabf.plot` will be
        useful to you. You don't have to import it, just call its functions
        and pass-in the abf object you're currently working with.

        Notice in this example there is an L-shaped scalebar. Nice!
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
        pyabf.plot.sweeps(abf, title=False, offsetXsec=.05,
                          offsetYunits=15, startAtSec=3, endAtSec=3.5)
        pyabf.plot.scalebar(abf, hideFrame=False)
        plt.tight_layout()
        self.saveAndClose()

    def demo_09a_digital_outputs(self):
        """
        ## Accessing Digital Outputs

        Epochs don't just control DAC clamp settings, they also control digital
        outputs. Digital outputs are stored as an 8-bit byte with 0 representing
        off and 1 representing on. Calling `abf.sweepD(digOutNum)` will return
        a waveform (scaled 0 to 1) to show the high/low state of the digital
        output number given (usually 0-7). Here a digital output controls an 
        optogenetic stimulator, and a light-evoked EPSC is seen several 
        milliseconds after the stimulus
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")

        fig = plt.figure(figsize=self.figsize)

        ax1 = fig.add_subplot(211)
        ax1.set_title("Digital Output 4")
        ax1.set_ylabel("State")

        # plot the digital output of the first sweep
        ax1.plot(abf.sweepX, abf.sweepD(4), color='r')

        ax2 = fig.add_subplot(212, sharex=ax1)
        ax2.set_title("Recorded Waveform")
        ax2.set_xlabel(abf.sweepLabelY)
        ax2.set_ylabel(abf.sweepLabelC)

        # plot the data from every sweep
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            ax2.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.8, lw=.5)

        fig.subplots_adjust(hspace=.4)
        ax2.axes.set_xlim(1.10, 1.25)
        ax2.axes.set_ylim(-150, 50)

        self.saveAndClose()

    def demo_10a_digital_output_shading(self):
        """
        ## Shading Digital Outputs

        Drawing digital outputs on the same graph as the data is a bit more
        subtle because it requires you to know the times digital outputs
        switch state (rather than the instantaneous state of the output at every
        point in time).

        Notice how much easier life gets when we don't deal with subplots.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")

        plt.figure(figsize=self.figsize)
        for sweepNumber in abf.sweepList:
            abf.setSweep(sweepNumber)
            plt.plot(abf.sweepX, abf.sweepY, color='C0', alpha=.8, lw=.5)
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.title("Shaded Digital Output #4")
        plt.axis([1.10, 1.25, -150, 50])

        outputStateByEpoch = abf.digitalWaveformEpochs[4]  # digital output 4
        for epochNumber, outputState in enumerate(outputStateByEpoch):
            if outputState == 1:
                t1 = abf.epochPoints[epochNumber]*abf.dataSecPerPoint
                t2 = abf.epochPoints[epochNumber+1]*abf.dataSecPerPoint
                plt.axvspan(t1, t2, color='r', alpha=.3, lw=0)

        self.saveAndClose()

    def demo_11a_gap_free(self):
        """
        ## Working with Gap-Free Files

        The pyABF project considers everything like it's an episodic ABF.
        Gap free ABF files are treated as if they were episodic files with
        a single sweep.

        When an abf object is instantiated, `setSweep(0)` is called
        automatically, so the entire gap-free set of data is pre-loaded into
        sweepX and sweepY.

        Note also that if it doesn't seem like the units are consistant
        with a simple current-clamp or voltage-clamp signal, the label
        is made from the channel name and the units.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/16d22006_kim_gapfree.abf")

        plt.figure(figsize=self.figsize)
        plt.plot(abf.sweepX, abf.sweepY, lw=.5)
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.title("Example Gap Free File")
        self.saveAndClose()

    def demo_12a_tags(self):
        """
        ## Accessing Comments (Tags) in ABF Files

        While recording an ABF the user can insert a comment at a certain
        time point. ClampFit calls these "tags", and they can be a useful
        way to mark things like drug applications during an experiment.

        A list of comments (the text of tags) is stored in a list 
        `abf.tagComments`. The sweep for each tag is in `abf.tagSweeps`, while
        the time of each tag is in `abf.tagTimesSec` and `abf.tagTimesMin`
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/16d05007_vc_tags.abf")

        # first plot the entire ABF continuously
        plt.figure(figsize=self.figsize)
        for sweep in abf.sweepList:
            abf.setSweep(sweep, absoluteTime=True)
            abf.sweepY[:int(abf.dataRate*1.0)] = np.nan  # blank the memtest
            plt.plot(abf.sweepX, abf.sweepY, lw=.5, color='C0')
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)

        # now add the tags as vertical lines
        for i, tagTimeSec in enumerate(abf.tagTimesSec):
            plt.axvline(abf.tagTimesSec[i], label=abf.tagComments[i],
                        color=f"C{i+3}", ls='--', alpha=.8)
        plt.legend()

        plt.title("ABF File Comments (Tags)")
        self.saveAndClose()

    def demo_13a_baseline(self):
        """
        ## Baseline Subtraction

        Sometimes it is worthwhile to center every sweep at 0. This can be done
        easily by running `abf.baseline(t1, t2)` (where t1 and t2 are both times
        in seconds). Subsequent `setSweep()` calls will automatically subtract
        the average data value between these two points from the entire sweep,
        centering it at zero.

        To turn off baseline subtraction after it has been enabled, call 
        `abf.baseline()` without arguments.
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
        plt.figure(figsize=self.figsize)

        # enable baseline subtraction and plot a demo sweep
        abf.baseline(2.1, 2.15)
        abf.setSweep(3)
        plt.plot(abf.sweepX, abf.sweepY, label="subtracted")

        # disable baseline subtraction and plot a demo sweep
        abf.baseline()
        abf.setSweep(3)
        plt.plot(abf.sweepX, abf.sweepY, label="original")

        # decorate the plot
        plt.title("Sweep Baseline Subtraction")
        plt.axhline(0, color='k', ls='--')
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.legend()
        plt.axis([2, 2.5, -50, 20])
        self.saveAndClose()

    def demo_14a_gaussian_filter(self):
        """
        ## Gaussian Filter (Lowpass Filter / Data Smoothing)

        Noisy data can be filtered in software. This is especially helpful
        for inspection of evoked or spontaneuos post-synaptic currents. To
        apply low-pass filtering on a specific channel, invoke the 
        `abf.filter.gaussian()` method a single time. After that, every
        `setSweep()` will display filtered data.

        The degree of smoothing is defined by _sigma_ (milliseconds units), 
        passed as an argument: `abf.filter.gaussian(abf, sigma)`. Increase
        sigma to increase the smoothness. Note that calling this filter 
        multiple times on the same ABF will make it progressively smoother, but
        the act is resource-intense and not recommended. 

        Set sigma to 0 to remove all filters (the original data will be re-read
        from the ABF file).
        """

        import pyabf
        abf = pyabf.ABF("data/abfs/17o05026_vc_stim.abf")
        plt.figure(figsize=self.figsize)

        # plot the original data
        abf.setSweep(3)
        plt.plot(abf.sweepX, abf.sweepY, alpha=.3, label="original")

        # show multiple degrees of smoothless
        for sigma in [.5, 2, 10]:
            pyabf.filter.gaussian(abf, 0)  # remove old filter
            pyabf.filter.gaussian(abf, sigma)  # apply custom sigma
            abf.setSweep(3)  # reload sweep
            plt.plot(abf.sweepX, abf.sweepY, alpha=.8, label=f"sigma: {sigma}")

        # zoom in on an interesting region
        plt.title("Gaussian Filtering")
        plt.ylabel(abf.sweepLabelY)
        plt.xlabel(abf.sweepLabelX)
        plt.axis([8.20, 8.30, -45, -5])
        plt.legend()
        self.saveAndClose()


def cleanDocstrings(s):
    s = s.strip()
    s = s.replace("\n        ", "\n")
    return s


def cleanCode(s):
    uses = Uses()
    s = s.replace("\n        ", "\n")
    s = s.replace("data/abfs/", "")
    s = s.replace("self.saveAndClose()", "plt.show()")
    s = s.replace("self.figsize", str(uses.figsize))
    s = s.split('"""', 2)[2].strip()
    return s


def go():

    # start by deleting the contents of the output folder
    for fname in glob.glob(os.path.dirname(__file__)+"/source/*.*"):
        os.remove(fname)

    # start the markdown output text
    md = """

# Getting Started with pyABF

This page is a collection of common tasks performed by pyABF.
They start out simple and increase in complexity.

  * All ABFs used are provided in  [the data folder](/data/)
  * These tests (and this output) are automated by [generate.py](generate.py)
  * Examples `import matplotlib.pyplot as plt`
  * Examples `import numpy as np`
  * Alternate color scheme provided with `plt.style.use('bmh')`
"""

    # then run each of the use case functions above
    uses = Uses()

    # determine if the developer is actively testing a single function
    testingOnly = False
    for functionName in sorted(dir(uses)):
        if "_test" in functionName:
            testingOnly = True

    for functionName in sorted(dir(uses)):
        if not functionName.startswith("demo_"):
            continue

        if testingOnly and not "_test" in functionName:
            continue

        # run the function
        print(f"executing {functionName}()")
        func = getattr(uses, functionName)
        func()

        # use the function docstring as the markdown text
        md += "\n\n"+cleanDocstrings(func.__doc__)

        # include the source code of the function
        md += "\n\n**Code:**\n\n```python\n"
        md += cleanCode(inspect.getsource(func))
        md += "\n```"

        # show the image if it exists
        imgName = functionName+".jpg"
        if os.path.exists(os.path.dirname(__file__)+"/source/"+imgName):
            md += f"\n\n**Output:**\n\n![source/{imgName}](source/{imgName})"

    # save the markdown page
    with open(os.path.dirname(__file__)+"/readme.md", 'w') as f:
        f.write(md)


if __name__ == "__main__":
    go()