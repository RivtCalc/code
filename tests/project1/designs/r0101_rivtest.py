from rivet.rivet_lib import *; setfiles(os.path.realpath(__file__))


# region 1
# %% section 1
i__(
    f"""| [s] function/section label | [p];[h];[x] | [i] file name | 
    |[design]| design name |[date],[pdf],[toc],[clean]| title block file |
    |[report]| report config file | 

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate system is attached as a modifier, as in Cartesian frame of
    reference. Sometimes the state of motion asfda asd s fdas sfdfasdfasdf is
    emphasized, as in rotating frame of reference. Sometimes

    | [figure] | filename | caption  | size |
    | [figure] | filename | caption  | size |
    
    | [text] | textfile  | spaces,[b],[i] |
    
    | [latex] | α = \integral(x^2,x,a,b) |
    
    | [math] | asciiformula |
    """
)

r__(
    f"""| a plot | [o] filename  |
    fig, ax1 = plt.subplots()
    t = np.arange(0.01, 10.0, 0.01)
    s1 = np.exp(t)
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('time (s)')
    
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

# endregion 1
# region 2
# %% section 2
v__(
    f"""
    | values abcd |
    Some text if needed

    a11 = 12.23*IN
    value description

    a22 = 12.2*LBS
    value description

    a33 = 14
    description
    """
)

e__(
    f"""| equations  abcd |
    Some introductory text.
    
    aa2 = a11*4
    equation description | units |2,2|

    aa22 = a11*5
    equation description | units |2,2|
    """
)

i__(
    f"""| some description [s]|
    This is a test γ = 2*Σ of the system and this is a further test
    and another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of reference"
    has led to a variety of terms. For example, sometimes the type of coordinate

    |[newpage]|

    The way it transforms to frames considered as related is emphasized as in
    Galilean frame of reference. Sometimes frames are distinguished by the scale of
    their observations, as in macroscopic and microscopic frames of reference.[1]
    """
)

# endregion 2
# region 3
# %% section 3
v__(
    f"""| some values |
    gg = 5.4*FT
    height of roof

    hh = 12.2
    height of balcony
    """
)

i__(
    f"""| text |
    this is a one liner 4 γ
    """
)

e__(
    f"""| some equations |
    xx1 = gg + 4
    xx2 = hh + 10
    """
)

# endregion 3
# region 4
# %% section 4
print(var_rivet_dict)