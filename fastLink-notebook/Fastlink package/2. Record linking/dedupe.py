import rpy2.robjects as r_objects
r = r_objects.r


# 4) Run fastlink
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
