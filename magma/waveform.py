try:
    import matplotlib.pyplot as plt
    import numpy as np

    def waveform(signals, labels):

        signals = np.transpose(np.array(signals))

        n = len(signals[0])

        nsignals = len(signals)

        t = np.repeat(0.5*np.arange(n+1),2)[1:-1]
        signals = [np.repeat(s,2) for s in signals]

        for i in range(nsignals):
            plt.text(-1.5, i+.25, labels[i])
            plt.plot(t, 0.5*signals[i]+i, 'r', linewidth = 2)

        # plt.xlim([0,n])
        # plt.ylim([-.25,nsignals])

        plt.gca().axis('off')
        plt.show()
except ImportError as e:
    def waveform(signals, labels):
        raise Exception("Please install matplotlib to use this feature.")
