


def prob_cue(Hi,Hj):
    pass

def prior(Ri,Rj):
    len = Ri.getCommonLen(Rj)
    total_len_i = Ri.getTotalBoundary()
    total_len_j = Rj.getTotalBoundary()
    total_len_min = min(total_len_i,total_len_j)
    return len/total_len_min


def likehood_intensity_p(Ri,Rj):
    delta = abs(Ri.getIntensity() - Rj.getIntensity())


def prob_sp_cue(Ri, Rj, cue):
    Likehood = Likehoods[cue]
    Likehood(Ri,Rj)

    p_sp = prior(Ri,Rj)
    p_sm = 1 - p_sp


def prob_sp(Hi, Hj):
    res = 0
    for cue in cues:
        res += prob_sp_cue(Hi,Hj,cue)
