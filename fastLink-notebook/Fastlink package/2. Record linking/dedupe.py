import pandas as pd
from common import analytics
from rpy2.robjects import globalenv
import rpy2.robjects as r_objects
r = r_objects.r


# 3.2) Run fastlink
def fl_dedupe(df_a, exclded_fields, string_distance, cut_a, cut_p):

    get_dedupes = r('''
          my_fl_dedupe <- function(df_a) {{        
              pasteT <- function(x) {{
                  x <- sort(x)
                  x <- paste(x, collapse = ",")
                  x
              }}
              varnames      <- colnames(csv)
              varnames      <- varnames[-which(varnames %in% c({0}))]
              invisible(capture.output(fl_out <- fastLink(dfA = csv, dfB = csv, varnames = varnames,
                                        stringdist.match = varnames, stringdist.method = '{1}', cut.a = {2}, 
                                        cut.p = c(0.80, {3}), dedupe.matches = TRUE, linprog.dedupe = FALSE,
                                        cond.indep = 'TRUE',
                                        n.cores = 8,
                                        verbose = 'TRUE')))
              inds_ab <- data.table(cbind(fl_out$matches$inds.a, fl_out$matches$inds.b))
              inds_ab[, `:=`(V3, pasteT(V2)), by = V1]
              inds_ab <- inds_ab[,.(V1, V3)]
              inds_ab <- inds_ab[!duplicated(inds_ab)]
              setnames(inds_ab, 'V3', 'V2')
              inds_ab <- unique(inds_ab[,list(V2)])
              structure(list(fl_out = fl_out, inds_ab = inds_ab))
          }}'''.format(exclded_fields, string_distance, cut_a, cut_p))
    return get_dedupes(df_a)


def process_dedupe(param_exclde_list, string_distance, cut_a, cut_p, param_exclde_str, s, col_names):

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

            return fl_flag, message, varnames, em_p_gamma_k_m, em_p_gamma_k_u, v2
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
