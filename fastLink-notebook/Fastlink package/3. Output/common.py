import matplotlib.pyplot as plt
import pandas as pd
from google.colab import auth
import gspread
from oauth2client.client import GoogleCredentials

# 4.1) Display results
def display_results(fields, max_no_dup, left, right, key_position):

    false_positives = 0
    true_positives = 0
    false_negatives = 0
    true_negatives = 0

    l_and_r = pd.DataFrame(columns=('key',) + fields)

    k = 0
    for i in range(left.shape[0]):
      dup = right[right['key'] == left.values[i][0]]
      l_and_r.loc[k] = left.loc[i]
      if len(dup) == 0:
        for h in range(left.shape[0]):
          neg_count = 0
          if left.values[h][key_position][:12] == left.values[i][key_position][:12]:
            neg_count = neg_count + 1
        if neg_count < 2:
          true_negatives = true_negatives + 1
        else:
          false_negatives = false_negatives + 1
        k = k + 1
      else:
        k = k + 1
        for j in range(len(dup)):
          l_and_r.loc[k] = dup.values[j]
          if left.values[i][key_position][:12] == dup.values[j][key_position][:12]:
            true_positives = true_positives + 1
          else:
            false_positives = false_positives + 1
          k = k + 1
      l_and_r.loc[k] = "========="
      k = k + 1
    return l_and_r, true_positives, false_positives, true_negatives, false_negatives


# 4.2) Recall, precision and F_score results
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


# 4.3) Display M and U values
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


# 4.4) Update data to a Google Spreadsheet
def add_to_gspread(run_count, l_and_r, true_positives, false_positives, true_negatives, false_negatives, precision, recall, f_score, string_distance, cut_a, cut_p, param_exclde_str, m_and_u, menu_3):

    auth.authenticate_user()
    gc = gspread.authorize(GoogleCredentials.get_application_default())

    sh = gc.create('Fastlink {0}: Run {1}'.format(menu_3.value, run_count))
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
