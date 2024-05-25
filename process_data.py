import pandas as pd
import glob
import os

SCORE_SUM_COL = "Сумма баллов"
PRIPROTY_COL = "Приоритет"

DIR_CODES_COL = "Направление подготовки"
COUNTS_REQUIRED_COL = "Количество требуемых людей"
COUNTS_COMMON_COL = "Общее количество людей"
AVER_SCORE_COL = "Средний балл"
COUNTS_COL = "Количество людей"
COUNT_TYPE_COL = "Тип количества"


def load_data(load_dir):
    res = {}

    print("Loading data:")

    for i in glob.glob(f"{load_dir}/*.xlsx"):
        dir_code = ".".join(os.path.basename(i).split(".")[:-1])
        print(f"Loading {dir_code}.xlsx")

        res[dir_code] = pd.read_excel(i)

    print("Data has been loaded")

    return res


def calc_ranges(table):
    return {
        "b_min": table[SCORE_SUM_COL].min(), 
        "b_max": table[SCORE_SUM_COL].max(), 
        "p_min": table[PRIPROTY_COL].min(), 
        "p_max": table[PRIPROTY_COL].max()
    }


def calc_ranges_common(tables_all):
    ranges = [calc_ranges(i) for i in tables_all.values()]

    return {
        "b_min": min([i["b_min"] for i in ranges]), 
        "b_max": max([i["b_max"] for i in ranges]), 
        "p_min": min([i["p_min"] for i in ranges]), 
        "p_max": max([i["p_max"] for i in ranges])
    }


def validate_filter_params(filter_params, ranges):
    if filter_params["b1"] < ranges["b_min"] or filter_params["b1"] > ranges["b_max"]:
        raise ValueError("b1 is out of range") 
    
    if filter_params["b2"] < ranges["b_min"] or filter_params["b2"] > ranges["b_max"]:
        raise ValueError("b2 is out of range") 
    
    if filter_params["p1"] < ranges["p_min"] or filter_params["p1"] > ranges["p_max"]:
        raise ValueError("p1 is out of range") 
    
    if filter_params["p2"] < ranges["p_min"] or filter_params["p2"] > ranges["p_max"]:
        raise ValueError("p2 is out of range") 
    
    if filter_params["b1"] > filter_params["b2"]:
        raise ValueError("b1 must be less than b2 or equal it")
    
    if filter_params["p1"] > filter_params["p2"]:
        raise ValueError("p1 must be less than p2 or equal it")


def filter_table(table, filter_params):
    b1 = filter_params["b1"]
    b2 = filter_params["b2"]
    p1 = filter_params["p1"]
    p2 = filter_params["p2"]
    
    part_need = table[(table[SCORE_SUM_COL] >= b1) & (table[SCORE_SUM_COL] <= b2) & \
                      (table[PRIPROTY_COL] >= p1) & (table[PRIPROTY_COL] <= p2)]
    
    return part_need


def create_stat_table(tables_all, filter_params, ranges):
    processed_tables = []

    for i in tables_all.keys():
        validate_filter_params(filter_params[i], ranges[i])
        processed_tables.append(filter_table(tables_all[i], filter_params[i]))

    counts_required = [i[SCORE_SUM_COL].count() for i in processed_tables]
    counts_common = [tables_all[i][SCORE_SUM_COL].count() for i in tables_all.keys()]
    score_average = []

    for i in range(len(processed_tables)):
        score_average.append(processed_tables[i][SCORE_SUM_COL].sum() / counts_required[i])

    frame_counts = pd.DataFrame({
        DIR_CODES_COL: list(tables_all.keys()),
        COUNTS_REQUIRED_COL: counts_required,
        COUNTS_COMMON_COL: counts_common,
        AVER_SCORE_COL: score_average,
    })

    return frame_counts


def reshape_counts_to_show(tables_all, table_counts):
    dir_codes = []
    counts = []
    count_type = []

    row_num = 0

    for i in tables_all.keys():
        dir_codes += [i, i]
        count_type += ["Требуемых", "Общее"]
        counts.append(table_counts[COUNTS_REQUIRED_COL][row_num])
        counts.append(table_counts[COUNTS_COMMON_COL][row_num])

        row_num = row_num + 1

    return pd.DataFrame({
        DIR_CODES_COL: dir_codes,
        COUNTS_COL: counts,
        COUNT_TYPE_COL: count_type
    })


def form_tables_with_required_people(tables_all, filter_params, ranges, save_dir):
    for dir_code, dir_df in tables_all.items():
        validate_filter_params(filter_params[dir_code], ranges[dir_code])

        b1 = filter_params[dir_code]["b1"]
        b2 = filter_params[dir_code]["b2"]
        p1 = filter_params[dir_code]["p1"]
        p2 = filter_params[dir_code]["p2"]

        name_suffix = f"{b1}_{b2}_{p1}_{p2}"

        save_path = f"{save_dir}/{dir_code}_{name_suffix}.xlsx"

        df_filtered = filter_table(dir_df, filter_params[dir_code])
        df_filtered.to_excel(save_path)