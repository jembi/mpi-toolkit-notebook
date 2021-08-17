import time
import pandas as pd
from dedupe import fl_dedupe
from rpy2.robjects import globalenv
import rpy2.robjects as r_objects
r = r_objects.r


# 4) Run fastlink
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


def record_link(param_exclde_list, string_distance, cut_a, cut_p, param_exclde_str, s, col_names):

    if len(param_exclde_list) != len(col_names):
        try:
            df_a = s
            globalenv['dedupes'] = fl_dedupe(df_a, param_exclde_str, string_distance, cut_a, cut_p)
            log_info = analytics('dedupes')
            varnames = log_info[0]
            em_p_gamma_k_m = log_info[1]
            em_p_gamma_k_u = log_info[2]
            v2 = tuple(r('dedupes$inds_ab$V2'))
            message = "Run successful"
            fl_flag = 2

            return fl_flag, message, varnames, em_p_gamma_k_m, em_p_gamma_k_u
        except IndexError:
            message = "Please increase the lower bound value in Section 3!"
            fl_flag = 1
            return fl_flag, message
    else:
        message = "Warning: You have exluded all fields in Section 3!\nOnly select the fields you want to 'EXCLUDE' from the Fastlink run"
        fl_flag = 0
        return fl_flag, message


def sort_records(col_names, v2, s_time):

    fields = tuple(col_names)
    left = pd.DataFrame(columns=('key',) + fields)
    right = pd.DataFrame(columns=('key',) + fields)
    k = 0
    max_no_dup = 0

    for i in range(len(v2)):
        dupe_links = tuple(map(int, v2[i].split(',')))
        if len(dupe_links) > max_no_dup:
            max_no_dup = len(dupe_links)
        dup = []
        master = r('csv[{},]'.format(dupe_links[0]))
        for j in range(1, len(dupe_links)):
            count_1 = 0
            for u in range(len(master)):
                if str(master.rx2(u + 1)[0]) == "NA":
                    count_1 += 1

            holder = r('csv[{},]'.format(dupe_links[j]))
            count_2 = 0
            for h in range(len(holder)):
                if str(holder.rx2(h + 1)[0]) == "NA":
                    count_2 += 1

            if count_1 > count_2:
                right.loc[k] = (i,) + tuple(map(lambda x: str(master.rx2(x)[0]), fields))
                k = k + 1
                master = holder
            else:
                right.loc[k] = (i,) + tuple(map(lambda x: str(holder.rx2(x)[0]), fields))
                k = k + 1
        left.loc[i] = (i,) + tuple(map(lambda x: str(master.rx2(x)[0]), fields))
    exec_time = (time.time() - s_time) / 60
    message = "Records have been sorted successfully"
    return message, fields, left, right, max_no_dup, exec_time

