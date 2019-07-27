#! python
# | [rivet] | calculation name | [date] |


#%%
r__(
    f"""| a caption plot [s] | filename [o] | [p] |
    fig, ax1 = plt.subplots()
    t = np.arange(0.01, 10.0, 0.01)
    s1 = np.exp(t)
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('time (s)')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('exp', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    s2 = np.sin(2 * np.pi * t)
    ax2.plot(t, s2, 'r.')
    ax2.set_ylabel('sin', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.show()
    """
)

i__(
    f"""| function label |
    The need to distinguish between  the various
    meanings of "frame of reference" has led to a variety of terms. For
    example, sometimes the type of coordinate system is attached as a
    modifier, as in Cartesian frame of reference. Sometimes the state of
    motion asfda asd s fdas sfdfasdfasdf is emphasized, as in rotating frame
    of reference. Sometimes

    | [figure] | filename | caption  | size | [d] |
    | [figure] | filename | caption  | size | [d] |
    | [insert] | textfile  | [i][b] |
    | [latex]  | \alpha = \integral(x^2,x,a,b) |
    | [math]   | asciiformula |
    """
)

# |newpage|

v__(
    f"""| values abcd  |
    a11 = 12*4  #|2, 2|
    a22 = 12.2
    a33 = 14
    """
)

e__(
    f"""equations  abcd     | ref
    aa2 = a11*4
    aa22 = a11*5
    """
)

#%% section 0
i__(
    f"""This is a test γ = 2*Σ of the system and this is a further test
    of the system and another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of reference"
    has led to a variety of terms. For example, sometimes the type of coordinate

    the way it transforms to frames considered as related is emphasized as in
    Galilean frame of reference. Sometimes frames are distinguished by the scale of
    their observations, as in macroscopic and microscopic frames of reference.[1]
    """
)

v__(
    f"""|some values |
    gg = 5.4    # height of roof {gam}   |    |
    hh = 12.2   # height of balcony |   |
    """
)

i__(
    f"""|text|
    this is a one liner 4 / {sig}
    """
)

e__(
    """|some equations |
    xx1 = gg + 4
    xx2 = hh + 10
    """
)
