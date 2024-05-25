const inputB1 = document.getElementById("input_b1");
const inputB2 = document.getElementById("input_b2");
const inputP1 = document.getElementById("input_p1");
const inputP2 = document.getElementById("input_p2");

const buttonCalcCount = document.getElementById("calc_count");
const buttonCalcPeople = document.getElementById("calc_people");

const plotCountsSpread = document.getElementById("plot_counts_spread");
const plotScoreSpread = document.getElementById("plot_score_spread");

const errorText = document.getElementById("error");

const b_min = Number(inputB1.getAttribute("min"));
const b_max = Number(inputB1.getAttribute("max"));
const p_min = Number(inputP1.getAttribute("min"));
const p_max = Number(inputP1.getAttribute("max"));

const resetError = () => errorText.textContent = "";

const validateParams = params => {
    if (params.b1 < b_min || params.b1 > b_max) return `значение b1 вне диапазона (${b_min}, ${b_max})`;
    if (params.b2 < b_min || params.b2 > b_max) return `значение b2 вне диапазона (${b_min}, ${b_max})`;
    if (params.p1 < p_min || params.p1 > p_max) return `значение p1 вне диапазона (${p_min}, ${p_max})`;
    if (params.p2 < p_min || params.p2 > p_max) return `значение p2 вне диапазона (${p_min}, ${p_max})`;

    if (params.b1 > params.b2) return "значение b1 не должно быть больше значения b2";
    if (params.p1 > params.p2) return "значение p1 не должно быть больше значения p2";

    return "success";
}

const getParams = () => ({
    b1: Number(inputB1.value),
    b2: Number(inputB2.value),
    p1: Number(inputP1.value),
    p2: Number(inputP2.value),
});

inputB1.addEventListener("change", resetError);
inputB2.addEventListener("change", resetError);
inputP1.addEventListener("change", resetError);
inputP2.addEventListener("change", resetError);

buttonCalcCount.addEventListener("click", async function () {
    let params = getParams();

    let valRes = validateParams(params);
    if (valRes !== "success") {
        errorText.textContent = valRes;
        return;
    } else resetError();

    let response = await fetch("/table_counts", {
        method: "POST",
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: JSON.stringify(params), 
    });

    if (response.status !== 200) {
        errorText.textContent = "Server error";
        return;
    }

    let plots_paths = await response.json();

    plotCountsSpread.setAttribute("src", plots_paths.counts_spread + "?" + new Date().getTime());
    plotScoreSpread.setAttribute("src", plots_paths.average_score_spread + "?" + new Date().getTime());
});

buttonCalcPeople.addEventListener("click", async function () {
    let params = getParams();

    let valRes = validateParams(params);
    if (valRes !== "success") {
        errorText.textContent = valRes;
        return;
    } else resetError();

    let response = await fetch("/people_required_for_every_table", {
        method: "POST",
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: JSON.stringify(params), 
    });

    if (response.status !== 200) {
        errorText.textContent = "Server error";
        return;
    }
});