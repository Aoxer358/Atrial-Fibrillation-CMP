settings = dict(
    structure=dict(
        size=(16, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=.97,
        y_coupling=.1,  # probability of y linkage
        z_coupling=.1,
        seed=None # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    ),
    viewer=dict(
        cross_view =True,
        save=False,  # save file?
        cross_pos=50,
        interval=1,  # length of each frame in milliseconds
    ),
    view='activation',
    crosspos=50,
    pause=False
)
