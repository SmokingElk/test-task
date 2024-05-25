import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from process_data import DIR_CODES_COL, COUNTS_COL, COUNT_TYPE_COL, AVER_SCORE_COL

matplotlib.use('Agg')


def create_counts_plot(counts_table, save_path):
	sns.set_style("whitegrid")

	plot = sns.catplot(
		data=counts_table,
		x=DIR_CODES_COL,
		y=COUNTS_COL,
		hue=COUNT_TYPE_COL,
		kind="bar",
		palette=sns.color_palette(["#9413cb", "#13CB85"])
	)

	plot.set(title="Распределение количества людей по направлениям подготовки")
	plot.set_xticklabels(rotation=30)

	plot.savefig(save_path)


def create_scores_plot(scores_table, save_path):
	sns.set_style("whitegrid")

	fig, ax = plt.subplots(figsize=(7, 7))
	ax.set_title("Средний суммарный балл по направлениям подготовки", fontsize=15)

	sns.barplot(
		data=scores_table,
		x=DIR_CODES_COL,
		y=AVER_SCORE_COL,
		ax=ax,
		color="#D9A7EF",
		edgecolor="#9413cb"
	)

	plt.xticks(rotation=30)

	fig.savefig(save_path)