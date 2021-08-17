import rpy2.robjects as r_objects
r = r_objects.r


# 4) Run fastlink
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
              fl_out <- fastLink(dfA = dfA, dfB = dfB, varnames = varnames,
                                  stringdist.match = varnames, stringdist.method = '{1}', cut.a = {2}, cut.p = {3},
                                  dedupe.matches = FALSE, linprog.dedupe = FALSE,
                                  cond.indep = TRUE,
                                  n.cores = 8,
                                  verbose = TRUE)
              inds_ab <- data.table(cbind(fl_out$matches$inds.a, fl_out$matches$inds.b))
              inds_ab[, `:=`(V3, pasteT(V2)), by = V1]
              inds_ab <- inds_ab[,.(V1, V3)]
              inds_ab <- inds_ab[!duplicated(inds_ab)]
              setnames(inds_ab, 'V3', 'V2')
              structure(list(fl_out = fl_out, inds_ab = inds_ab))
          }}'''.format(exclded_fields, string_distance, cut_a, cut_p))
    return get_links(df_a, df_b)
