import numpy as np
import math

import Region

def get_sparseness(R):
   G = R.getHist()
   # n1 = norm_1(G)
   n1 = 1
   n2 = np.linalg.norm(G,ord=2)
   n = len(G)-1
   if n == 1:
       return 2
   S = (1/(math.sqrt(n)-1))*(math.sqrt(n)-n1/n2)
   return S

def prob_cue_R(R):
    sparseness = get_sparseness(R)

    a = 41.9162
    b = -37.1885

    res = 1/(1-math.exp(-(a*sparseness+b)))

    return res

def prob_cue_1(Ri,Rj):
    p_cue_ri = prob_cue_R(Ri)
    p_cue_rj = prob_cue_R(Rj)
    res = min(p_cue_ri,p_cue_rj)
    return res

def prior(Ri,Rj):
    len = Region.getCommonLen(Ri,Rj)
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

    sigma_noise = 1
    simga_scale = sigma_noise/math.sqrt(omega_min)

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
    sigma_noise = 1
    simga_scale = sigma_noise/math.sqrt(omega_min)
    sigma_m_ij = sigma_m_local+simga_scale

    res = normpdf(delta_ij,0,sigma_m_ij)

    return res

def chi_square(x,k):
    res = 1/(math.pow(2,k/2)*math.gamma(k/2))*math.pow(x,k/2-1)*math.exp(-x/2)
    return res


def likehood_texture_p(Ri,Rj):
    Dij = Region.getTextureDifference(Ri,Rj)
    #degree of freedom
    k = 4

    Dip = Ri.getTextureDifferenceP()
    Djp = Rj.getTextureDifferenceP()

    alpha_p = (k-2)/(min(Dip,Djp))

    res = chi_square(Dij*alpha_p,k)

    return res

def likehood_texture_m(Ri,Rj):
    Dij = Region.getTextureDifference(Ri,Rj)
    #degree of freedom
    k = 4

    Dim = Ri.getTextureDifferenceM()
    Djm = Rj.getTextureDifferenceM()

    alpha_m = (k-2)/((Dim+Djm)/2)

    res = chi_square(Dij*alpha_m,k)

    return res


likehoods_p = {"intensity":likehood_intensity_p,"texture":likehood_texture_p}
likehoods_m = {"intensity":likehood_intensity_m,"texture":likehood_texture_m}

def prob_sp_cue(Ri, Rj, cue):
    likehood_p = likehoods_p[cue]
    likehood_m = likehoods_m[cue]
    lm = likehood_m(Ri,Rj)
    lp = likehood_p(Ri,Rj)

    p_sp = prior(Ri,Rj)
    p_sm = 1 - p_sp

    res = lp*p_sp/(lp*p_sp+lm*p_sm)

    return res

#main function
def prob_sp(Ri, Rj):
    res = 0
    cues = ["intensity","texture"]
    #cues = ["texture"]
    for cue in cues:
        p_cue = prob_cue_1(Ri,Rj)
        if cue == "texture":
            p_cue = 1 - p_cue
        res += prob_sp_cue(Ri,Rj,cue)*p_cue
    return res
