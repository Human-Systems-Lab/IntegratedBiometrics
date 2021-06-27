from typing import List, Tuple, Optional

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

import ibs

# |-----|-----|-----|
# |  0  |  T  |  1  |
# |-----|-----|-----|
# |  L  |  C  |  R  |
# |-----|-----|-----|
# |  3  |  B  |  2  |
# |-----|-----|-----|

Left = 0
Top = 1
Right = 2
Bottom = 3

mappings = {                             #  L0   T0   T1   R1   R2   B2   B3   L3
    ibs.LayoutHint.Center:       np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),

    ibs.LayoutHint.Left:         np.array([0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5], dtype=np.float32),
    ibs.LayoutHint.Top:          np.array([0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.Right:        np.array([0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.Bottom:       np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0], dtype=np.float32),

    ibs.LayoutHint.LeftFull:     np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=np.float32),
    ibs.LayoutHint.TopFull:      np.array([0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.RightFull:    np.array([0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.BottomFull:   np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0], dtype=np.float32),

    ibs.LayoutHint.LeftTop:      np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.TopLeft:      np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.TopRight:     np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.RightTop:     np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.RightBottom:  np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.BottomLeft:   np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.BottomRight:  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.LeftBottom:   np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=np.float32),

    ibs.LayoutHint.LeftCenter:   np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.TopCenter:    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.RightCenter:  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.BottomCenter: np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),

    ibs.LayoutHint.LeftFloat:    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.TopFloat:     np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.RightFloat:   np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32),
    ibs.LayoutHint.BottomFloat:  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)
}


# n?*[lw]  <- Naming convention (not [left/right/top/bottom])(direction)(layout/widget)

# noinspection PyArgumentList
def nl_layout(ccaps, cw, tw, rw, bw) -> QLayout:
    if ccaps[1] == Top:
        if ccaps[2] == Right:
            nlbcl = QVBoxLayout()
            nlbcl.addWidget(cw)
            nlbcl.addWidget(bw)
            nlbcw = QWidget()
            nlbcw.setLayout(nlbcl)

            nlbl = QHBoxLayout()
            nlbl.addWidget(nlbcw)
            nlbl.addWidget(rw)
            nlbw = QWidget()
            nlbw.setLayout(nlbl)

        elif ccaps[2] == Bottom:
            nlrcl = QHBoxLayout()
            nlrcl.addWidget(cw)
            nlrcl.addWidget(rw)
            nlrcw = QWidget()
            nlrcw.setLayout(nlrcl)

            nlbl = QVBoxLayout()
            nlbl.addWidget(nlrcw)
            nlbl.addWidget(bw)
            nlbw = QWidget()
            nlbw.setLayout(nlbl)
        else:
            raise ValueError("Invalid value for ccaps[2]")

        layout = QVBoxLayout()
        layout.addWidget(tw)
        layout.addWidget(nlbw)
        return layout
    elif ccaps[2] == Bottom:
        assert(ccaps[1] == Right)

        nltcl = QVBoxLayout()
        nltcl.addWidget(tw)
        nltcl.addWidget(cw)
        nltcw = QWidget()
        nltcw.setLayout(nltcl)

        nltl = QHBoxLayout()
        nltl.addWidget(nltcw)
        nltl.addWidget(rw)
        nltw = QWidget()
        nltw.setLayout(nltl)

        layout = QVBoxLayout()
        layout.addWidget(tw)
        layout.addWidget(nltw)
        return layout
    else:
        assert(ccaps[1] == Right and ccaps[2] == Right)
        nlcl = QVBoxLayout()
        nlcl.addWidget(tw)
        nlcl.addWidget(cw)
        nlcl.addWidget(bw)
        nlcw = QWidget()
        nlcw.setLayout(nlcl)

        layout = QHBoxLayout()
        layout.addWidget(nlcw)
        layout.addWidget(rw)
        return layout


# noinspection PyArgumentList
def nt_layout(ccaps, cw, lw, rw, bw) -> QLayout:
    if ccaps[2] == Right:
        if ccaps[3] == Bottom:
            ntlcl = QHBoxLayout()
            ntlcl.addWidget(lw)
            ntlcl.addWidget(cw)
            ntlcw = QWidget()
            ntlcw.setLayout(ntlcl)

            ntll = QVBoxLayout()
            ntll.addWidget(ntlcw)
            ntll.addWidget(bw)
            ntlw = QWidget()
            ntlw.setLayout(ntlw)

        elif ccaps[3] == Left:
            ntbcl = QVBoxLayout()
            ntbcl.addWidget(cw)
            ntbcl.addWidget(bw)
            ntbcw = QWidget()
            ntbcw.setLayout(ntbcl)

            ntll = QHBoxLayout()
            ntll.addWidget(lw)
            ntll.addWidget(ntbcw)
            ntlw = QWidget()
            ntlw.setLayout(ntlw)
        else:
            raise ValueError("Invalid value for ccaps[2]")

        layout = QHBoxLayout()
        layout.addWidget(ntlw)
        layout.addWidget(rw)
        return layout
    elif ccaps[3] == Left:
        assert (ccaps[2] == Bottom)

        ntrcl = QHBoxLayout()
        ntrcl.addWidget(cw)
        ntrcl.addWidget(rw)
        ntrcw = QWidget()
        ntrcw.setLayout(ntrcl)

        ntrl = QVBoxLayout()
        ntrl.addWidget(ntrcw)
        ntrl.addWidget(bw)
        ntrw = QWidget()
        ntrw.setLayout(ntrl)

        layout = QHBoxLayout()
        layout.addWidget(lw)
        layout.addWidget(ntrw)
        return layout
    else:
        assert (ccaps[2] == Bottom and ccaps[3] == Bottom)
        ntcl = QHBoxLayout()
        ntcl.addWidget(lw)
        ntcl.addWidget(cw)
        ntcl.addWidget(rw)
        ntcw = QWidget()
        ntcw.setLayout(ntcl)

        layout = QVBoxLayout()
        layout.addWidget(ntcw)
        layout.addWidget(bw)
        return layout


# noinspection PyArgumentList
def nr_layout(ccaps, cw, lw, tw, bw) -> QLayout:
    if ccaps[3] == Bottom:
        if ccaps[0] == Left:
            nrtcl = QVBoxLayout()
            nrtcl.addWidget(tw)
            nrtcl.addWidget(cw)
            nrtcw = QWidget()
            nrtcw.setLayout(nrtcl)

            nrtl = QHBoxLayout()
            nrtl.addWidget(lw)
            nrtl.addWidget(nrtcw)
            nrtw = QWidget()
            nrtw.setLayout(nrtw)

        elif ccaps[0] == Top:
            nrlcl = QHBoxLayout()
            nrlcl.addWidget(lw)
            nrlcl.addWidget(cw)
            nrlcw = QWidget()
            nrlcw.setLayout(nrlcl)

            nrtl = QVBoxLayout()
            nrtl.addWidget(tw)
            nrtl.addWidget(nrlcw)
            nrtw = QWidget()
            nrtw.setLayout(nrtw)
        else:
            raise ValueError("Invalid value for ccaps[2]")

        layout = QVBoxLayout()
        layout.addWidget(nrtw)
        layout.addWidget(bw)
        return layout
    elif ccaps[0] == Top:
        assert (ccaps[3] == Left)

        nrbcl = QVBoxLayout()
        nrbcl.addWidget(cw)
        nrbcl.addWidget(bw)
        nrbcw = QWidget()
        nrbcw.setLayout(nrbcl)

        nrbl = QHBoxLayout()
        nrbl.addWidget(lw)
        nrbl.addWidget(nrbcw)
        nrbw = QWidget()
        nrbw.setLayout(nrbl)

        layout = QVBoxLayout()
        layout.addWidget(tw)
        layout.addWidget(nrbw)
        return layout
    else:
        assert (ccaps[3] == Left and ccaps[0] == Left)
        nrcl = QVBoxLayout()
        nrcl.addWidget(tw)
        nrcl.addWidget(cw)
        nrcl.addWidget(bw)
        nrcw = QWidget()
        nrcw.setLayout(nrcl)

        layout = QHBoxLayout()
        layout.addWidget(lw)
        layout.addWidget(nrcw)
        return layout


# noinspection PyArgumentList
def nb_layout(ccaps, cw, lw, tw, rw) -> QLayout:
    if ccaps[0] == Left:
        if ccaps[1] == Top:
            nbrcl = QHBoxLayout()
            nbrcl.addWidget(cw)
            nbrcl.addWidget(rw)
            nbrcw = QWidget()
            nbrcw.setLayout(nbrcl)

            nbrl = QVBoxLayout()
            nbrl.addWidget(tw)
            nbrl.addWidget(nbrcw)
            nbrw = QWidget()
            nbrw.setLayout(nbrl)

        elif ccaps[1] == Right:
            nbtcl = QVBoxLayout()
            nbtcl.addWidget(tw)
            nbtcl.addWidget(cw)
            nbtcw = QWidget()
            nbtcw.setLayout(nbtcl)

            nbrl = QHBoxLayout()
            nbrl.addWidget(nbtcw)
            nbrl.addWidget(rw)
            nbrw = QWidget()
            nbrw.setLayout(nbrl)
        else:
            raise ValueError("Invalid value for ccaps[2]")

        layout = QHBoxLayout()
        layout.addWidget(lw)
        layout.addWidget(nbrw)
        return layout
    elif ccaps[1] == Right:
        assert (ccaps[0] == Top)

        nblcl = QHBoxLayout()
        nblcl.addWidget(lw)
        nblcl.addWidget(cw)
        nblcw = QWidget()
        nblcw.setLayout(nblcl)

        nbll = QVBoxLayout()
        nbll.addWidget(tw)
        nbll.addWidget(nblcw)
        nblw = QWidget()
        nblw.setLayout(nbll)

        layout = QHBoxLayout()
        layout.addWidget(nblw)
        layout.addWidget(rw)
        return layout
    else:
        assert (ccaps[0] == Top and ccaps[1] == Top)
        nbcl = QHBoxLayout()
        nbcl.addWidget(lw)
        nbcl.addWidget(cw)
        nbcl.addWidget(rw)
        nbcw = QWidget()
        nbcw.setLayout(nbcl)

        layout = QVBoxLayout()
        layout.addWidget(tw)
        layout.addWidget(nbcw)
        return layout


# noinspection PyArgumentList
def arrange_sidepanel(idx, widgets) -> QLayout:
    if idx % 2 == 0:
        layout = QVBoxLayout()
    else:
        layout = QHBoxLayout()

    for i in [2, 0, 1, 4, 3]:
        for e in widgets[i]:
            layout.addWidget(e)
    return layout


# noinspection PyArgumentList
def arrange_center(widgets) -> QLayout:
    # TODO: Improve this algorithm and optionally add 2 layers to l/t/r/b
    layout = QHBoxLayout()
    for e in widgets:
        layout.addWidget(e)
    return layout


# noinspection PyArgumentList
def build_layout(exts: List[Optional[Tuple[QWidget, ibs.LayoutHint]]]) -> QLayout:
    # Filtering the extensions for widgets
    guicfgs: List[Tuple[QWidget, ibs.LayoutHint]] = [e for e in exts if e is not None]

    # Building the main widgets from extension widgets

    # Creating the 5 main widgets which make up the screen
    cw = QWidget()
    lw = QWidget()
    tw = QWidget()
    rw = QWidget()
    bw = QWidget()

    # Sorting the extension widgets by location
    center_widgets = list()
    widget_types = [[list() for _ in range(5)] for _ in range(4)]  # [l,t,r,b][std,ful,beg,end,flo]
    for guicfg in guicfgs:
        lo = guicfg[1]
        if lo == 0:
            center_widgets.append(guicfg[0])
        elif (lo - 1) % 6 == 5:
            # *Center LayoutHint type
            raise NotImplementedError("*Center type hints have not been implemented yet")
        else:
            widget_types[(lo - 1) // 6][(lo - 1) % 6].append(guicfg[0])

    for i, (panel, widgets) in enumerate(zip([lw, tw, rw, bw], widget_types)):
        panel.setLayout(arrange_sidepanel(i, widgets))
    cw.setLayout(arrange_center(center_widgets))

    # Arranging the main widgets into a single QLayout

    # Corner allocation
    corners = np.zeros((8,), dtype=np.float32)
    for guicfg in guicfgs:
        corners += mappings[guicfg[1]]
    ccaps = [4] * 4
    for i in range(4):
        if corners[2 * i] > corners[2 * i + 1]:
            ccaps[i] = i  # 0->L, 1->T, 2->R, 3->B
        elif corners[2 * i] < corners[2 * i + 1]:
            ccaps[i] = (i + 1) % 4  # 0->T, 1->R, 2->B, 3->L
        else:
            ccaps[i] = 2 * (i // 2) + 1  # Prioritizing top/bottom over left/right

    # Checking for rotational symetry (That layout is not buildable in PyQt5)
    # If it occurs, it gets resolved by restricting the top panel
    if ccaps == [i for i in range(4)]:
        ccaps[1] = Right
    if ccaps == [(i + 1) % 4 for i in range(4)]:
        ccaps[0] = Left

    # Looking for a duplicate capture as a starting point
    ccount = [0] * 4
    for i in ccaps:
        ccount[i] += 1
    cstart = 4
    for i in range(4):
        if ccount == 2:
            cstart = i
            break

    if cstart == 0:
        tmp = QWidget()
        tmp.setLayout(nl_layout(ccaps, tw, rw, bw))
        layout = QHBoxLayout()
        layout.addWidget(lw)
        layout.addWidget(tmp)
    elif cstart == 1:
        tmp = QWidget()
        tmp.setLayout(nt_layout(ccaps, cw, lw, rw, bw))
        layout = QVBoxLayout()
        layout.addWidget(tw)
        layout.addWidget(tmp)
    elif cstart == 2:
        tmp = QWidget()
        tmp.setLayout(nr_layout(ccaps, cw, lw, tw, bw))
        layout = QHBoxLayout()
        layout.addWidget(tmp)
        layout.addWidget(rw)
    elif cstart == 3:
        tmp = QWidget()
        tmp.setLayout(nb_layout(ccaps, cw, lw, tw, rw))
        layout = QVBoxLayout()
        layout.addWidget(tmp)
        layout.addWidget(bw)
    else:
        layout = QHBoxLayout()
        layout.addWidget(cw)

    return layout
