import pandas as pd
import glob
import os

SCORE_SUM_COL = "Сумма баллов"
PRIPROTY_COL = "Приоритет"

OUT_PATH = "out"


def read_all():
    res = {}

    print("Loading data:")

    for i in glob.glob("data/*.xlsx"):
        dir_code = ".".join(os.path.basename(i).split(".")[:-1])
        print(f"Loading {dir_code}.xlsx")

        res[dir_code] = pd.read_excel(i)

    print("Data has been loaded")

    return res


def calc_ranges(tables_all):
    b_min = min([i[SCORE_SUM_COL].min() for i in tables_all.values()])
    b_max = max([i[SCORE_SUM_COL].max() for i in tables_all.values()])
    p_min = min([i[PRIPROTY_COL].min() for i in tables_all.values()])
    p_max = max([i[PRIPROTY_COL].max() for i in tables_all.values()])
    return b_min, b_max, p_min, p_max


def process_table(table, b1, b2, p1, p2):
    part_need = table[(table[SCORE_SUM_COL] >= b1) & (table[SCORE_SUM_COL] <= b2) & (table[PRIPROTY_COL] >= p1) & (table[PRIPROTY_COL] <= p2)]
    return part_need


def form_table_counts(tables_all, b1, b2, p1, p2):
    processed_tables = [process_table(tables_all[i], b1, b2, p1, p2) for i in tables_all.keys()]
    counts = [i[SCORE_SUM_COL].count() for i in processed_tables]
    score_average = []

    for i in range(len(processed_tables)):
        score_average.append(processed_tables[i][SCORE_SUM_COL].sum() / counts[i])

    frame_counts = pd.DataFrame({
        "Направление подготовки": list(tables_all.keys()),
        "Количество людей": counts,
        "Средний балл": score_average,
    })

    return frame_counts


def create_counts_to_show(tables_all, table_counts):
    dir_codes = []
    counts = []
    count_type = []

    row_num = 0

    for i in tables_all.keys():
        dir_codes.append(i)
        dir_codes.append(i)
        counts.append(table_counts["Количество людей"][row_num])
        counts.append(tables_all[i][SCORE_SUM_COL].count())
        count_type.append("По параметрам")
        count_type.append("Общее")

        row_num = row_num + 1

    return pd.DataFrame({
        "Направление подготовки": dir_codes,
        "Количество людей": counts,
        "Тип количества": count_type
    })


def form_tables_with_required_people(tables_all, b1, b2, p1, p2):
    for dir_code, dir_df in tables_all.items():
        save_path = f"{OUT_PATH}/{dir_code}_{b1}_{b2}_{p1}_{p2}.xlsx"

        df_filtered = process_table(dir_df, b1, b2, p1, p2)
        df_filtered.to_excel(save_path)