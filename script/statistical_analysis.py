import numpy as np
import pandas as pd
import scipy.stats as stats
from os import listdir
from os.path import join
import re
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import warnings

warnings.filterwarnings("ignore")


def parse_files(path, pattern, target, columns, verbose=True):
    configs = {}

    for file in listdir(path):
        # Buscamos todos los ficheros de resultados para la instancia concreta
        if re.match(pattern, file):
            key = file[file.find("y_") + 2 : file.find(".allHV")]
            data = np.loadtxt(join(path, file))
            configs[key] = data

    print(configs)
    if configs:
        df = pd.DataFrame.from_dict(configs)
        df = df[columns]

        df = df.replace(0, np.nan)
        if df[target].isnull().any():
            return pd.DataFrame()
        return df
    else:
        return pd.DataFrame()


def compare_samples(sample_1, sample_2, alpha=0.05):
    final_p_value = 0
    _, p_value_levene = stats.levene(sample_1, sample_2)
    if p_value_levene >= alpha:
        _, p_value_anova = stats.f_oneway(sample_1, sample_2)
        final_p_value = p_value_anova
        test_name = "ANOVA"
    else:
        _, p_value_welch = stats.ttest_ind(sample_1, sample_2)
        final_p_value = p_value_welch
        test_name = "WELCH"

    return (final_p_value, test_name)


def stats_procedure(data, target, keys, alpha=0.05):
    """
    Esta función sigue el funcionamiento
    básico del fichero de estadísticas de METCO
    con nombre statisticalTests_old.pl
    """
    p_values = {k: stats.shapiro(data[k]).pvalue for k in data.columns}

    # Calculamos media y mediana
    df_mean = data.mean()
    df_median = data.median()

    # Realizamos una comparación de cada configuración contra el resto
    df = pd.DataFrame(columns=keys)
    results = []
    """
        Representa las victorias y empates de la configuracion
        target contra las otras configuraciones en la lista keys
        Los valores [x, y] representan:
        - x: Las victorias del target contra la configuracion
        - y: Los empates del target contra la configuracion
    """
    wins_draws = {k: [0, 0] for k in keys}
    for other in keys:
        if other == target:
            continue
        if data[other].isnull().any():
            """
            Los datos de la configuracion 'other' fueron todo
            ceros, lo que implica que no pudo conseguir soluciones
            factibles en el tiempo especificado
            """
            results.append(df_mean[target])
            wins_draws[other][0] += 1
            continue

        final_p_value = 0
        # Comprobamos que todas las muestras siguen normalidad
        if p_values[target] >= alpha and p_values[other] >= alpha:
            final_p_value, test_name = compare_samples(data[target], data[other])
        else:  # En caso de una distribución no Normal, usamos Kruskal Wallis
            _, final_p_value = stats.kruskal(data[target], data[other])
        # Comprobamos hipótesis
        if final_p_value < alpha:
            if df_mean[target] > df_mean[other] or df_median[target] > df_median[other]:
                wins_draws[other][0] += 1
            else:
                wins_draws[other][1] += 1

        # No hay diferencia
        else:
            results.append(-1)
            wins_draws[other][1] += 1

    df.loc[0] = wins_draws  # Ponemos los resultados en el DF
    f = [item for s in list(wins_draws.values()) for item in s]

    return df, f, results


def plot_differences(df, figure_name):
    df = df.loc[valids]
    df = df.reset_index(drop=True)
    fig, axis = plt.subplots(1, 3, figsize=(30, 10))

    kwargs = dict(hist_kws={"alpha": 0.6}, kde_kws={"linewidth": 2})

    # , title='Performance difference between GA_0.7 and GA_0.8')
    colors = ["blue", "darkorange", "green"]
    for i, key in enumerate(df.columns):
        sns.histplot(df[key], color=colors[i], label=key, kde=True, ax=axis[i], bins=10)

        axis[i].title.set_text(f"Performance difference between {key}")
        axis[i].set(xlabel="Difference", ylabel="Frequency")
        axis[i].legend(loc="upper right")

    plt.savefig(figure_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statistical Analysis")
    parser.add_argument("path", type=str, help="Path where the .allHV files are stored")
    parser.add_argument("ver_df", type=str, help="Name of the verification dataset")
    parser.add_argument("diff_df", type=str, help="Name of the differences dataset")

    args = parser.parse_args()
    path = args.path

    df = pd.read_csv(join(path, args.ver_df), index_col=0)
    diff_df = pd.read_csv(join(path, args.diff_df), index_col=0)

    valids = []
    keys = df.columns.to_list()
    target = keys[0]
    keys_stats = keys[1:]

    comp_df = pd.DataFrame(columns=keys)
    table = []
    text_table = []
    n_instances = df.index.to_list()
    for i in n_instances:
        # TODO: Update pattern to match the files
        pattern = rf"instance_{i}_target_GA_1.0_solved_by_GA_\d\.\d\.allHV"
        i_configs = parse_files(path, pattern, target, keys, True)
        if not i_configs.empty:
            valids.append(i)
            rs, row, avg_row = stats_procedure(
                i_configs, target, keys_stats, alpha=0.05
            )
            comp_df = pd.concat([comp_df, rs], ignore_index=True)
            table.append(row)

    results = np.array(table).sum(axis=0)
    print(results)
    i = 0
    for case in diff_df.columns:
        print(
            f'- {case.replace("-", " vs ")}: Wins {results[i]} No-diff: {results[i + 1]}'
        )
        i += 2

    figure_name = f"differences_target_{target}_others.png"
    plot_differences(diff_df, figure_name)
