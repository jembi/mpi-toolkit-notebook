import matplotlib.pyplot as plt
import pandas as pd
from google.colab import auth
import gspread
from oauth2client.client import GoogleCredentials


# 5.1) Display results
def display_results(fields, max_no_dup, left, right, key_position):

    false_positives = 0
    true_positives = 0
    false_negatives = 0
    true_negatives = 0

    col = (('key',) + fields) * max_no_dup
    l_and_r = pd.DataFrame(columns=col)
    empty_tup = ("",) * len(('key',) + fields)

    for i in range(left.shape[0]):
        pop_tup = ()
        pop_tup = tuple(left.values[i])
        count = 0
        for j in range(right.shape[0]):
            if right.values[j][0] == left.values[i][0]:
                pop_tup = pop_tup + tuple(right.values[j])
                count = count + 1
                if left.values[i][key_position][:12] == right.values[j][key_position][:12]:
                    true_positives = true_positives + 1
                else:
                    false_positives = false_positives + 1
        pop_tup = pop_tup + (empty_tup * ((max_no_dup - 1) - count))
        if (max_no_dup - 1) - count == 3:
            for k in range(len(left)):
                neg_count = 0
                if left.values[k][key_position][:12] == pop_tup[key_position][:12]:
                    neg_count = neg_count + 1
            if neg_count < 2:
                true_negatives = true_negatives + 1
            else:
                false_negatives = false_negatives + 1
        l_and_r.loc[i] = pop_tup
    return l_and_r, true_positives, false_positives, true_negatives, false_negatives


# 5.2) Recall, precision and F_score results
def analytics(true_positives, false_positives, false_negatives):

    recall = true_positives/(true_positives + false_negatives)
    recall_labels = ["Recall", " "]
    recall_sections = [recall, 1 - recall]

    precision = true_positives/(true_positives + false_positives)
    prec_labels = ["Precision", " "]
    prec_sections = [precision, 1 - precision]

    f_score = 2 * ((precision * recall)/(precision + recall))
    f_labels = ["F_score", " "]
    f_sections = [f_score, 1 - f_score]

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
    colors = ["#6396e6", "#de73e6"]

    axes[0].pie(recall_sections,
                labels=recall_labels,
                colors=colors,
                startangle=90,
                autopct='%1.4f%%')
    axes[1].pie(prec_sections,
                labels=prec_labels,
                colors=colors,
                startangle=90,
                autopct='%1.4f%%')
    axes[2].pie(f_sections,
                labels=f_labels,
                colors=colors,
                startangle=90,
                autopct='%1.4f%%')

    plt.title("Pie charts showing Recall, Precision and F_score")
    return recall, precision, f_score


# 5.3) Display M and U values
def weights(em_p_gamma_k_m, em_p_gamma_k_u):

    fields = ("Field", "Matches (M)", "Unmatches (U)")
    m_and_u = pd.DataFrame(columns=fields)
    for i in range(len(em_p_gamma_k_m)):
        m_and_u.loc[i] = (em_p_gamma_k_m[i][1], em_p_gamma_k_m[i][3], em_p_gamma_k_u[i][3])
    table_1 = m_and_u.style.format({"Matches (M)": "{:.4f}",
                                    "Unmatches (U)": "{:.4f}"}) \
        .hide_index() \
        .set_properties(**{'text-align': 'left'})
    table_1 = table_1.set_table_styles(
        [dict(selector='th', props=[('text-align', 'left')])])
    return table_1, m_and_u


# 5.4) Update data to a Google Spreadsheet
def add_to_gspread(run_count, l_and_r, true_positives, false_positives, true_negatives, false_negatives, precision, recall, f_score, string_distance, cut_a, cut_p, param_exclde_str, m_and_u):

    auth.authenticate_user()
    gc = gspread.authorize(GoogleCredentials.get_application_default())

    sh = gc.create('Fastlink Dedupe: Run {0}'.format(run_count))
    ws = sh.add_worksheet(title="Results", rows="100", cols="100")
    sh.del_worksheet(sh.sheet1)
    ws.update([l_and_r.columns.values.tolist()] + l_and_r.values.tolist())

    ws = sh.add_worksheet(title="Configuration and Performance", rows="10", cols="20")
    ws.update("A1:K1", [["True Positives", "False Positives", "True Negatives",
                         "False Negatives", "Precision", "Recall", "F Score",
                         "String Distance Method", "Cut.a", "Cut.p", "Parameters excluded"]])
    ws.update("A2:K2", [[true_positives, false_positives, true_negatives,
                         false_negatives, precision, recall, f_score,
                         string_distance, cut_a, cut_p, param_exclde_str]])

    ws = sh.add_worksheet(title="M and U values", rows="30", cols="10")
    ws.update([m_and_u.columns.values.tolist()] + m_and_u.values.tolist())
    message = "Data saved to Google Drive"
    return message
