from flask import Flask, request, render_template
from process_data import read_all, form_table_counts, form_tables_with_required_people, OUT_PATH, calc_ranges, create_counts_to_show
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from json import dumps
from gevent import sleep
from gevent.pywsgi import WSGIServer
import os

HOST = "127.0.0.1"
PORT = 3000

matplotlib.use('Agg')

app = Flask(__name__, static_folder="static", template_folder="static")
ui_server = WSGIServer((HOST, PORT), app, log=open(os.devnull, "w"))

frames = read_all()
b_min, b_max, p_min, p_max = calc_ranges(frames)


@app.route('/', methods=['GET'])
def root():
    return render_template("index.html", b_min=b_min, b_max=b_max, p_min=p_min, p_max=p_max)


@app.route('/table_counts', methods=['POST'])
def table_counts():
    params = request.get_json()
    frame_counts = form_table_counts(frames, params["b1"], params["b2"], params["p1"], params["p2"])

    frame_counts[["Направление подготовки", "Количество людей"]].to_excel(f"{OUT_PATH}/common.xlsx")
    
    counts_save_path = "static/counts_spread.png"
    counts_to_show = create_counts_to_show(frames, frame_counts)

    sns.set_style("whitegrid")

    plot = sns.catplot(
        data=counts_to_show,
        x="Направление подготовки",
        y="Количество людей",
        hue="Тип количества",
        kind="bar",
        palette=sns.color_palette(["#9413cb", "#13CB85"])
    )

    plot.set(title="Распределение количества людей по направлениям подготовки")
    plot.set_xticklabels(rotation=30)

    plot.savefig(counts_save_path)
    plot.set

    score_save_path = "static/average_score_spread.png"

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_title("Средний суммарный балл по направлениям подготовки", fontsize=15)

    sns.barplot(
        data=frame_counts,
        x="Направление подготовки",
        y="Средний балл",
        ax=ax,
        color="#D9A7EF",
        edgecolor="#9413cb"
    )

    plt.xticks(rotation=30)

    fig.savefig(score_save_path)

    return dumps({"counts_spread": counts_save_path, "average_score_spread": score_save_path})


@app.route('/people_required_for_every_table', methods=['POST'])
def tables_with_people():
    params = request.get_json()
    form_tables_with_required_people(frames, params["b1"], params["b2"], params["p1"], params["p2"])

    return "ok"   

if __name__ == "__main__":
    print(f"UI is running on http://{HOST}:{PORT}")
    ui_server.start()

    while True:
        sleep(60)