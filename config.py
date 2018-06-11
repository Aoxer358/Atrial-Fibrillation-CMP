settings = dict(
    structure=dict(
        size=[25, 200, 200],  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=[0,1],
        yz_coupling=[0,1],  # probability of y linkage

        seed=None # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=60,  # pacemaker activation period
        runtime=1000,
    ),
    viewer=dict(
        cross_view =True,
        save=False,  # save file?
        cross_pos=50,
        interval=1,  # length of each frame in milliseconds
    ),
    v_cross_pos=50,
    h_cross_pos=50,
    w_cross_pos=1,
)
