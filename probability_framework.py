import numpy as np
import math

import Region

SIGMA_NOISE = 7
CUES = ["intensity","texture"]
# CUES = ["texture"]
#CUES = ["intensity"]


#texture probability utils
def getHist(pixels):
    pixels = [1]
    return np.bincount(pixels,minlength=256)/len(pixels)


def get_sparseness(R):
   pixels = R.getPixels()

   G = getHist(pixels)

   norm1 = np.linalg.norm(G,ord=1)
   norm2 = np.linalg.norm(G,ord=2)
   n = len(G)

   S = (1/(math.sqrt(n)-1))*(math.sqrt(n)-norm1/norm2)
   return S

def prob_cue_R(R):
    sparseness = get_sparseness(R)

    a = 41.9162
    b = -37.1885

    if -(a*sparseness+b) < 0:
        pass

    pow = -(a*sparseness+b)

    if pow>700:
        pow = 700

    res = 1/(1-math.exp(pow))
    if res < 0:
        res = 0
    if res > 1:
        res = 1
    if res == 0:
        #print()
        pass
    return res

def prob_cue_1(Ri,Rj):
    p_cue_ri = prob_cue_R(Ri)
    p_cue_rj = prob_cue_R(Rj)
    res = min(p_cue_ri,p_cue_rj)
    if res==0:
        #print()
        pass
    return res


#prior
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

    sigma_noise = SIGMA_NOISE
    simga_scale = sigma_noise/math.sqrt(omega_min)

    sigma_p_ij = sigma_p_local+simga_scale

    res = normpdf(delta_ij,0,sigma_p_ij)

    if Ri.value != Rj.value:
        # print()
        pass

    if not Ri.pixel:
        # print()
        pass

    return res

def likehood_intensity_m(Ri,Rj):
    delta_ij = abs(Ri.getIntensity() - Rj.getIntensity())

    delta_m_i = Ri.externalMDifference()
    delta_m_j = Rj.externalMDifference()

    sigma_m_local = (delta_m_i+delta_m_j)/2


    omega_i = Ri.getTotalPixels()
    omega_j = Rj.getTotalPixels()
    omega_min = min(omega_i,omega_j)
    sigma_noise = SIGMA_NOISE
    simga_scale = sigma_noise/math.sqrt(omega_min)
    sigma_m_ij = sigma_m_local+simga_scale

    res = normpdf(delta_ij,0,sigma_m_ij)

    if Ri.value != Rj.value:
        # print()
        pass

    if not Ri.pixel:
        # print()
        pass

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

    minD = min(Dip,Djp)

    alpha_p = 0
    res = 0

    if not Ri.pixel:
        #print()
        pass

    if minD == 0 and Dij == 0:
        alpha_p = k - 2
        res = chi_square(alpha_p, k)
    else:
        if minD == 0:
            minD = 0.1
        alpha_p = (k-2)/(minD)
        res = chi_square(Dij / alpha_p, k)


    # if res ==0:
    #     print("Error?")
    return res

def likehood_texture_m(Ri,Rj):
    Dij = Region.getTextureDifference(Ri,Rj)
    #degree of freedom
    k = 4

    Dim = Ri.getTextureDifferenceM()
    Djm = Rj.getTextureDifferenceM()

    mean = (Dim+Djm)/2
    if mean == 0:
        mean = 0.1

    alpha_m = (k-2)/(mean)

    res = chi_square(Dij/alpha_m,k)

    # if res ==0:
    #     print("Error?")

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

    # if (lp*p_sp+lm*p_sm) == 0:
    #     print("Error")

    res = lp*p_sp/(lp*p_sp+lm*p_sm)

    if not Ri.pixel:
        # print()
        pass

    if Ri.value != Rj.value:
        # print()
        pass

    return res

#main function
def prob_sp(Ri, Rj):
    res = 0
    for cue in CUES:
        p_cue = prob_cue_1(Ri,Rj)
        if cue == "texture":
            p_cue = 1 - p_cue
            if p_cue != 0:
                # print()
                pass
        prob_sp_cue_p = prob_sp_cue(Ri,Rj,cue)
        res += prob_sp_cue_p*p_cue
    return res
