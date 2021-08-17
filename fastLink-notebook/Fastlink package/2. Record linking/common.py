import time
import pandas as pd
from rpy2.robjects import globalenv
import rpy2.robjects as r_objects
r = r_objects.r


# 3.2) Run fastlink
def capture_user_input(menu_1, check_b_list, menu_2, slider_1):

    s_time = time.time()
    key = menu_1.value
    key_position = menu_1.index + 1
    string_distance = menu_2.value
    if string_distance == "Jaro-Winkler":
        string_distance = "jw"
    elif string_distance == "Jaro":
        string_distance = "jaro"
    else:
        string_distance = "lv"
    cut_a = slider_1.value[0]
    cut_p = slider_1.value[1]

    param_exclde_list = []
    for i in range(len(check_b_list)):
        if check_b_list[i].value == True:
            param_exclde_list.append(check_b_list[i].description)

    param_exclde_str = "'"
    for k in range(len(param_exclde_list)):
        if k < len(param_exclde_list) - 1:
            param_exclde_str = param_exclde_str + param_exclde_list[k] + "', '"
        else:
            param_exclde_str = param_exclde_str + param_exclde_list[k] + "' "

    return s_time, key, key_position, string_distance, cut_a, cut_p, param_exclde_list, param_exclde_str


def analytics(process):

    varnames = tuple(globalenv['{0}'.format(process)].rx2('fl_out').rx2('EM').rx2('varnames'))
    em_p_gamma_k_m = []
    for i in range(len(r('{0}$fl_out$EM$p.gamma.k.m'.format(process)))):
        placeholder = ['p.gamma.k.m ----- %-20s : %3.10f  %3.10f  %3.10f',
                       varnames[i],
                       r('{0}$fl_out$EM$p.gamma.k.m'.format(process))[i][0],
                       abs(r('{0}$fl_out$EM$p.gamma.k.m'.format(process))[i][1]),
                       r('{0}$fl_out$EM$p.gamma.k.m'.format(process))[i][0] + r('{0}$fl_out$EM$p.gamma.k.m'.format(process))[i][1]]
        em_p_gamma_k_m.append(placeholder)
    em_p_gamma_k_u = []
    for i in range(len(r('{0}$fl_out$EM$p.gamma.k.u'.format(process)))):
        placeholder = ['p.gamma.k.u ----- %-20s : %3.10f  %3.10f  %3.10f',
                       varnames[i],
                       abs(r('{0}$fl_out$EM$p.gamma.k.u'.format(process))[i][0]),
                       r('{0}$fl_out$EM$p.gamma.k.u'.format(process))[i][1],
                       r('{0}$fl_out$EM$p.gamma.k.u'.format(process))[i][0] + r('{0}$fl_out$EM$p.gamma.k.u'.format(process))[i][1]]
        em_p_gamma_k_u.append(placeholder)
    return varnames, em_p_gamma_k_m, em_p_gamma_k_u
