


def prob_cue(Hi,Hj):
    pass

def prior(Ri,Rj):
    len = Ri.getCommonLen(Rj)
    total_len_i = Ri.getTotalBoundary()
    total_len_j = Rj.getTotalBoundary()
    total_len_min = min(total_len_i,total_len_j)
    return len/total_len_min

def normpdf(x, mean, sd):
    var = float(sd)**2
    pi = 3.1415926
    denom = (2*pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def likehood_intensity_p(Ri,Rj):
    delta_ij = abs(Ri.getIntensity() - Rj.getIntensity())

    delta_p_i = Ri.externalPDifference()
    delta_p_j = Rj.externalPDifference()

    sigma_p_local = min(delta_p_i,delta_p_j)

    omega_i = Ri.getTotalPixels()
    omega_j = Rj.getTotalPixels()

    omega_min = min(omega_i,omega_j)

    simga_scale = sigma_noise/sqrt(omega_min)

    sigma_p_ij = sigma_p_local+simga_scale

    res = normpdf(delta_ij,0,sigma_p_ij)

    return res

def likehood_intensity_m(Ri,Rj):
    delta_ij = abs(Ri.getIntensity() - Rj.getIntensity())

    delta_m_i = Ri.externalMDifference()
    delta_m_j = Rj.externalMDifference()

    sigma_m_local = (delta_m_i+delta_m_j)/2


    omega_i = Ri.getTotalPixels()
    omega_j = Rj.getTotalPixels()
    omega_min = min(omega_i,omega_j)
    simga_scale = sigma_noise/sqrt(omega_min)
    sigma_m_ij = sigma_m_local+simga_scale

    res = normpdf(delta_ij,0,sigma_m_ij)

    return res


def prob_sp_cue(Ri, Rj, cue):
    Likehood = Likehoods[cue]
    Likehood(Ri,Rj)

    p_sp = prior(Ri,Rj)
    p_sm = 1 - p_sp


def prob_sp(Hi, Hj):
    res = 0
    for cue in cues:
        res += prob_sp_cue(Hi,Hj,cue)
