from common import analytics
import time
import os
import pandas as pd
from rpy2.robjects import globalenv
from rpy2.robjects.vectors import StrVector
import rpy2.robjects as r_objects
import rpy2.robjects.packages as r_packages
r = r_objects.r

# 3.2) Run fastlink
def fl_link(df_a, df_b, exclded_fields, string_distance, cut_a, cut_p):

    get_links = r('''
          my_fl_link <- function(dfA, dfB) {{
              pasteT <- function(x) {{
                  x <- sort(x)
                  x <- paste(x, collapse = ",")
                  x
              }}
                
              varnames <- colnames(dfA)
              varnames <- varnames[-which(varnames %in% c({0}))]
              invisible(capture.output(fl_out <- fastLink(dfA = dfA, dfB = dfB, varnames = varnames,
                                  stringdist.match = varnames, stringdist.method = '{1}', cut.a = {2}, cut.p = {3},
                                  dedupe.matches = FALSE, linprog.dedupe = FALSE,
                                  cond.indep = TRUE,
                                  n.cores = 8,
                                  verbose = TRUE)))
              inds_ab <- data.table(cbind(fl_out$matches$inds.a, fl_out$matches$inds.b))
              inds_ab[, `:=`(V3, pasteT(V2)), by = V1]
              inds_ab <- inds_ab[,.(V1, V3)]
              inds_ab <- inds_ab[!duplicated(inds_ab)]
              setnames(inds_ab, 'V3', 'V2')
              structure(list(fl_out = fl_out, inds_ab = inds_ab))
          }}'''.format(exclded_fields, string_distance, cut_a, cut_p))
    return get_links(df_a, df_b)


def process_link(param_exclde_list, string_distance, cut_a, cut_p, param_exclde_str, s, col_names):

    if len(param_exclde_list) != len(col_names):
        try:
            df_a = r('dfA')
            df_b = r('dfB')
            globalenv['links'] = fl_link(df_a, df_b, param_exclde_str, string_distance, cut_a, cut_p)
            log_info = analytics('links')
            varnames = log_info[0]
            em_p_gamma_k_m = log_info[1]
            em_p_gamma_k_u = log_info[2]
            v1 = tuple(map(int, r('links$inds_ab$V1')))
            v2 = tuple(r('links$inds_ab$V2'))
            message = "Run successful"
            fl_flag = 2

            return fl_flag, message, varnames, em_p_gamma_k_m, em_p_gamma_k_u, v1, v2
        except IndexError:
            message = "Please increase the lower bound value in Section 3!"
            fl_flag = 1
            return fl_flag, message
    else:
        message = "Warning: You have exluded all fields in Section 3!\nOnly select the fields you want to 'EXCLUDE' from the Fastlink run"
        fl_flag = 0
        return fl_flag, message


def sort_links(col_names, v1, v2, s_time):

    fields = tuple(col_names)
    left = pd.DataFrame(columns=('key',) + fields)
    right = pd.DataFrame(columns=('key',) + fields)

    r('write.csv(dfA, file="df_a.csv")')
    p_df_a = pd.read_csv('df_a.csv')
    try:
      os.remove('df_a.csv')
    except OSError:
      pass
    k = 0
    max_no_dup = 0

    key = []
    for k in range(len(p_df_a)):
      key.append(k)

    p_df_a.insert(0, "key", key, True)
    for u in range(len(fields)):
      p_df_a[fields[u]] = p_df_a[fields[u]].astype(str)

    for i in range(len(p_df_a)):
      left.loc[i] = p_df_a.loc[i]
      for b in range(len(v1)):
        if int(v1[b]) == (i + 1):
          try:
            dupe_links = tuple(map(int, v2[b].split(',')))
          except IndexError:
            dupe_links = int(v2[b])
          for j in range(len(dupe_links)):
            if j + 2 > max_no_dup:
              max_no_dup = j + 2
            dup = r('dfB[{},]'.format(dupe_links[j]))
            right.loc[k] = (i,) + tuple(map(lambda x: str(dup.rx2(x)[0]), fields))
            k = k + 1
    exec_time = (time.time() - s_time) / 60
    message = "Records have been sorted successfully"
    return message, fields, left, right, max_no_dup, exec_time
