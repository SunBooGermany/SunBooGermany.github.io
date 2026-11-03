def under_paired_subplots(fig,name):
    old_legends=list(fig.legends)
    handles=[list(legend.legend_handles) for legend in old_legends]
    labels=[[t.get_text() for t in legend.get_texts()] for legend in old_legends]
    for legend in old_legends:legend.remove()
    pairs=[]
    if name=='figure_A2_matched_convergence':
        height=7.0
        fig.set_size_inches(6.5,height)
        for i,ax in enumerate(fig.axes):
            row,col=divmod(i,2)
            pos=ax.get_position()
            bottom=6.78-row*1.62-.86
            ax.set_position([pos.x0,bottom/height,pos.width,.86/height])
            if col==0:ax.set_ylabel('Normalized\ndistance',linespacing=1.05)
        for row in range(4):
            leg=fig.legend(handles=handles[0],labels=labels[0],loc='upper center',
                bbox_to_anchor=(.54,.5),borderaxespad=0,frameon=False,
                ncol=4,fontsize=9.2,handlelength=2.0,handletextpad=.55,
                columnspacing=1.25,labelspacing=.30)
            pairs.append((fig.axes[row*2:row*2+2],leg))
    else:
        height=5.3
        fig.set_size_inches(6.5,height)
        for i,ax in enumerate(fig.axes):
            row,col=divmod(i,2)
            pos=ax.get_position()
            bottom=3.43 if row==0 else .92
            panel_height=1.65 if row==0 else 1.73
            ax.set_position([pos.x0,bottom/height,pos.width,panel_height/height])
        for row in range(2):
            leg=fig.legend(handles=handles[row],labels=labels[row],loc='upper center',
                bbox_to_anchor=(.54,.5),borderaxespad=0,frameon=False,
                ncol=5 if row==0 else 4,fontsize=9.2,handlelength=1.5,handletextpad=.5,
                columnspacing=1.0,labelspacing=.35)
            pairs.append((fig.axes[row*2:row*2+2],leg))
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    # Anchor just below the actual tick/x-label extents, including log exponents.
    for axes,leg in pairs:
        label_boxes=[]
        for ax in axes:
            label_boxes.extend(t.get_window_extent(renderer) for t in ax.get_xticklabels() if t.get_visible())
            if ax.get_xlabel():label_boxes.append(ax.xaxis.label.get_window_extent(renderer))
        center=(axes[0].get_position().x0+axes[1].get_position().x1)/2
        leg.set_bbox_to_anchor((center,
            (min(b.y0 for b in label_boxes)-5)/fig.bbox.height),transform=fig.transFigure)
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    assert len(fig.legends)==len(fig.axes)//2
    boxes=[]
    for axes,leg in pairs:
        box=leg.get_window_extent(renderer)
        tickboxes=[]
        for ax in axes:
            tickboxes.extend(t.get_window_extent(renderer) for t in ax.get_xticklabels() if t.get_visible())
            if ax.get_xlabel():tickboxes.append(ax.xaxis.label.get_window_extent(renderer))
        assert box.y1<min(b.y0 for b in tickboxes)-1, 'Legend overlaps x-axis labels'
        boxes.append(box)
    for i,b in enumerate(boxes):
        for j,ax in enumerate(fig.axes):
            assert not b.overlaps(ax.get_window_extent(renderer)), 'Legend overlaps a panel'
            for label in ax.texts:
                assert not b.overlaps(label.get_window_extent(renderer)), (name,i,j,label.get_text(),b.bounds,label.get_window_extent(renderer).bounds)
    placements[name]=dict(subplots=len(fig.axes),common_legends=len(boxes),subplots_per_legend=2,
                         all_below_x_axis_labels=True,no_legend_or_axes_overlap=True,
                         figure_inches=[6.5,height])
    original_save(fig,name)
