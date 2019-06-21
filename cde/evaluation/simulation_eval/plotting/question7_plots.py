from ml_logger import logger

from cde.model_fitting.GoodnessOfFitResults import GoodnessOfFitResults
from cde.evaluation.simulation_eval import base_experiment
import cde.model_fitting.ConfigRunner as ConfigRunner
import matplotlib.pyplot as plt
import os

EXP_PREFIX = "question7_regularization_logprob"
RESULTS_FILE = "results.pkl"
CLUSTER_DIR = "/local/rojonas/cde/data/local"
LOCATION = "{}/{}/{}".format(CLUSTER_DIR, EXP_PREFIX, RESULTS_FILE)
DATA_DIR_LOCAL = "/home/jonasrothfuss/Dropbox/Eigene_Dateien/ETH/02_Projects/02_Noise_Regularization/02_Code_Conditional_Density_Estimation/data/cluster"

logger.configure(
    #"/local/rojonas/cde/data/local",
    DATA_DIR_LOCAL,
    EXP_PREFIX,
)

results_from_pkl_file = dict(logger.load_pkl_log(RESULTS_FILE))
gof_result = GoodnessOfFitResults(single_results_dict=results_from_pkl_file)
results_df = gof_result.generate_results_dataframe(base_experiment.KEYS_OF_INTEREST_LOGPROB)
results_df.replace(to_replace=[None], value="None", inplace=True)


# seprarate 2d and 4d GMM

results_df.index = list(range(len(results_df)))

for i, row in results_df[['simulator', 'ndim_y']].iterrows():
    if row['simulator'] == 'GaussianMixture':
        results_df.at[i, 'simulator'] = '%s_%id'%(row['simulator'], row['ndim_y'])

estimators = [
    "MixtureDensityNetwork",
    "KernelMixtureNetwork",
    "NormalizingFlowEstimator"
]
simulators = ["EconDensity", "GaussianMixture_2d", "GaussianMixture_4d", "SkewNormal"]

def _resize_plots(fig):
    fig.axes[0].set_ylim((-3, -1.9))
    #fig.axes[1].set_ylim((-7, -4.5))
    fig.axes[3].set_ylim((1.0, 1.63))

FIGSIZE = (15, 4.5)

# rules of thumb
# for estimator in estimators:
#     plot_dict = dict(
#         [
#             (
#                 simulator,
#                 {
#                     "rule_of_thumb_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "rule_of_thumb_1.00"
#                     },
#                     "rule_of_thumb_0.7": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "rule_of_thumb_0.70"
#                     },
#                     "rule_of_thumb_0.5": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "rule_of_thumb_0.50"
#                     },
#                     "rule_of_thumb_0.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "rule_of_thumb_0.00"
#                     },
#                     "quadratic_rate_2.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "quadratic_rate_2.00"
#                     },
#                     "quadratic_rate_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "quadratic_rate_1.00"
#                     },
#                 },
#             )
#             for simulator in simulators
#         ]
#     )
#     fig = gof_result.plot_metric(
#         plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 4), log_scale_y=False
#     )
#     _resize_plots(fig)
#     plt.suptitle('Regularization %s'%estimator)
#     fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_adaptive_noise_%s.png"%estimator))
#
# for estimator in estimators:
#     plot_dict = dict(
#         [
#             (
#                 simulator,
#                 {
#                     "weight_decay_0.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "weight_decay": 0.0
#                     },
#                     "weight_decay_0.001": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "weight_decay": 0.001
#                     },
#                     "weight_decay_0.01": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "weight_decay": 0.01
#                     },
#                     "weight_decay_0.1": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "weight_decay": 0.1
#                     },
#                 },
#             )
#             for simulator in simulators
#         ]
#     )
#     fig = gof_result.plot_metric(
#         plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 4), log_scale_y=False
#     )
#     _resize_plots(fig)
#     plt.suptitle('Regularization %s'%estimator)
#     fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_weight_decay_%s.png"%estimator))
#
#
# for estimator in estimators:
#     plot_dict = dict(
#         [
#             (
#                 simulator,
#                 {
#                     "l2_reg_0.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 0.0
#                     },
#                     "l2_reg_0.001": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 0.001
#                     },
#                     "l2_reg_0.01": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 0.01
#                     },
#                     "l2_reg_0.1": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 0.01
#                     },
#                     "l2_reg_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 1.0
#                     },
#                 },
#             )
#             for simulator in simulators
#         ]
#     )
#     fig = gof_result.plot_metric(
#         plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 4), log_scale_y=False
#     )
#     _resize_plots(fig)
#     plt.suptitle('Regularization %s'%estimator)
#     fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_l2_%s.png"%estimator))
#
# for estimator in estimators:
#     plot_dict = dict(
#         [
#             (
#                 simulator,
#                 {
#                     "l1_reg_0.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 0.0
#                     },
#                     "l1_reg_0.001": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 0.001
#                     },
#                     "l1_reg_0.01": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 0.01
#                     },
#                     "l1_reg_0.1": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 0.01
#                     },
#                     "l1_reg_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 1.0
#                     },
#                 },
#             )
#             for simulator in simulators
#         ]
#     )
#     fig = gof_result.plot_metric(
#         plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 4), log_scale_y=False
#     )
#     _resize_plots(fig)
#     plt.suptitle('Regularization %s'%estimator)
#     fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_l1_%s.png"%estimator))


# for estimator in estimators:
#     plot_dict = dict(
#         [
#             (
#                 simulator,
#                 {
#                     "rule_of_thumb_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "rule_of_thumb_1.00"
#                     },
#                     "quadratic_rate_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "adaptive_noise_fn": "quadratic_rate_1.00"
#                     },
#                     "l1_reg_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l1_reg": 1.0
#                     },
#                     "l2_reg_1.0": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "l2_reg": 1.0
#                     },
#                     "weight_decay_0.01": {
#                         "simulator": simulator,
#                         "estimator": estimator,
#                         "weight_decay": 0.01
#                     },
#                 },
#             )
#             for simulator in simulators
#         ]
#     )
#
#     fig = gof_result.plot_metric(
#         plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 4), log_scale_y=False
#     )
#     fig.axes[0].set_ylim((-2.3, -1.95))
#     fig.axes[3].set_ylim((1.5, 1.615))
#     plt.suptitle('Regularization %s'%estimator)
#     fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.png"%estimator))
#


#
# # Econ Density
# simulator = 'EconDensity'
# plot_dict = dict(
#     [
#         (
#             estimator,
#             {
#                 "noise_reg (ours)": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "rule_of_thumb_0.70" if estimator == "NormalizingFlowEstimator" else "rule_of_thumb_1.00"
#                 },
#                 "l1_reg_1.0": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l1_reg": 1.0
#                 },
#                 "l2_reg_1.0": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l2_reg": 1.0
#                 },
#                 "weight_decay_0.01": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "weight_decay": 0.01
#                 },
#                 "no_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "rule_of_thumb_0.00"
#                 },
#             },
#         )
#         for estimator in estimators
#     ]
# )
#
# fig = gof_result.plot_metric(
#     plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 3), log_scale_y=False
# )
# fig.axes[0].set_ylim((-2.8, -1.95))
# fig.axes[1].set_ylim((-2.8, -1.95))
# fig.axes[2].set_ylim((-2.8, -1.95))
#
#
# # fig.axes[3].set_ylim((1.5, 1.615))
# plt.suptitle('Regularization %s'%simulator)
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.png"%simulator))
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.pdf"%simulator))
#
#
#
# # Skew Norm
# simulator = 'SkewNormal'
# plot_dict = dict(
#     [
#         (
#             estimator,
#             {
#                 "noise_reg (ours)": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "polynomial_rate_2_2.00" if estimator == "KernelMixtureNetwork" else (
#                         "polynomial_rate_2_1.00" if estimator == "NormalizingFlowEstimator" else "polynomial_rate_3_1.00"
#                     ),
#                 },
#                 "l1_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l1_reg": 1.0
#                 },
#                 "l2_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l2_reg": 1.0
#                 },
#                 "weight_decay": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "weight_decay": 0.00 if estimator == "KernelMixtureNetwork" else 0.01
#                 },
#                 "no_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "rule_of_thumb_0.00"
#                 },
#             },
#         )
#         for estimator in estimators
#     ]
# )
#
# fig = gof_result.plot_metric(
#     plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 3), log_scale_y=False
# )
# fig.axes[0].set_ylim((1.0, 1.61))
# fig.axes[1].set_ylim((1.0, 1.61))
# fig.axes[2].set_ylim((1.0, 1.61))
#
#
# # fig.axes[3].set_ylim((1.5, 1.615))
# plt.suptitle('Regularization - Skew Normal')
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.png"%simulator))
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.pdf"%simulator))
#
#
# # Gaussian Mixture
# simulator = 'GaussianMixture_2d'
# plot_dict = dict(
#     [
#         (
#             estimator,
#             {
#                 "noise_reg (ours)": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "quadratic_rate_1.00",
#                     "weight_normalization": False
#                 },
#                 "l1_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l1_reg": 0.1 if estimator == "MixtureDensityNetwork" else 1.0
#                 },
#                 "l2_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "l2_reg": 0.1 if estimator == "MixtureDensityNetwork" else 1.0
#                 },
#                 "weight_decay": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "weight_decay": 0.001
#                 },
#                 "no_reg": {
#                     "simulator": simulator,
#                     "estimator": estimator,
#                     "adaptive_noise_fn": "rule_of_thumb_0.00"
#                 },
#             },
#         )
#         for estimator in estimators
#     ]
# )
#
# fig = gof_result.plot_metric(
#     plot_dict, metric="score", figsize=FIGSIZE, layout=(1, 3), log_scale_y=False
# )
# fig.axes[0].set_ylim((-6.5, -2.9))
# fig.axes[1].set_ylim((-6.5, -2.9))
# fig.axes[2].set_ylim((-6.5, -2.9))
#
#
# plt.suptitle('Regularization - Gaussian Mixture')
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.png"%simulator))
# fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_%s.pdf"%simulator))


# Gaussian Mixture & SkewNorm

plot_dict = dict(
    [
        (
            estimator,
            {
                "no_reg": {
                    "simulator": 'GaussianMixture_2d',
                    "estimator": estimator,
                    "adaptive_noise_fn": "rule_of_thumb_0.00"
                },
                "l1_reg": {
                    "simulator": 'GaussianMixture_2d',
                    "estimator": estimator,
                    "l1_reg": 0.1 if estimator == "MixtureDensityNetwork" else 1.0
                },
                "l2_reg": {
                    "simulator": 'GaussianMixture_2d',
                    "estimator": estimator,
                    "l2_reg": 0.1 if estimator == "MixtureDensityNetwork" else 1.0
                },
                "weight_decay": {
                    "simulator": 'GaussianMixture_2d',
                    "estimator": estimator,
                    "weight_decay": 0.00 if estimator == "KernelMixtureNetwork" else 0.01
                },
                "noise_reg (ours)": {
                    "simulator": 'GaussianMixture_2d',
                    "estimator": estimator,
                    "adaptive_noise_fn": "quadratic_rate_1.00",
                    "weight_normalization": False
                },
            },
        )
        for estimator in estimators
    ] + [
        (
            estimator + "_skew",
            {  "no_reg": {
                    "simulator": 'SkewNormal',
                    "estimator": estimator,
                    "adaptive_noise_fn": "rule_of_thumb_0.00"
                },
                "l1_reg": {
                    "simulator": 'SkewNormal',
                    "estimator": estimator,
                    "l1_reg": 1.0
                },
                "l2_reg": {
                    "simulator": 'SkewNormal',
                    "estimator": estimator,
                    "l2_reg": 1.0
                },
                "weight_decay": {
                    "simulator": 'SkewNormal',
                    "estimator": estimator,
                    "weight_decay": 0.001 if estimator == "KernelMixtureNetwork" else 0.01
                },
                "noise_reg (ours)": {
                    "simulator": 'SkewNormal',
                    "estimator": estimator,
                    "adaptive_noise_fn": "polynomial_rate_2_2.00" if estimator == "KernelMixtureNetwork" else (
                        "polynomial_rate_2_1.00" if estimator == "NormalizingFlowEstimator" else "polynomial_rate_3_1.00"
                    ),
                },
            },
        )
        for estimator in estimators
    ]
)


colors = iter(['#1f77b4', '#2ca02c', '#9467bd', '#ff7f0e', '#d62728'])

fig = gof_result.plot_metric(
    plot_dict, metric="score", figsize=(12, 6), layout=(2, 3), log_scale_y=False, color=colors
)

for i in range(0, 3):
    fig.axes[i].set_ylim((-6.5, -2.9))

for i in range(3, 6):
    fig.axes[i].set_ylim((1.0, 1.61))

for i in range(6):
    fig.axes[i].set_title("")
    fig.axes[i].set_xlabel('')
    fig.axes[i].set_ylabel('')
    fig.axes[i].get_legend().remove()

fig.axes[0].set_title("Mixture Density Network")
fig.axes[1].set_title("Kernel Mixture Network")
fig.axes[2].set_title("Normalizing Flow")

fig.axes[0].set_xlabel('number of train observations')
fig.axes[0].set_ylabel('log-likelihood')

fig.axes[0].annotate("Gaussian Mixture", xy=(0, 0.5), xytext=(-fig.axes[0].yaxis.labelpad - 6.0, 0),
                xycoords=fig.axes[0].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center', rotation=90)
fig.axes[3].annotate("Skew Normal", xy=(0, 0.5), xytext=(-fig.axes[0].yaxis.labelpad - 22.0, 0),
                xycoords=fig.axes[3].yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center', rotation=90)
plt.legend(["noise_reg (ours)", "l1_reg", "l2_reg", "weight_decay", "no_reg"])
fig.tight_layout()


plt.legend(["no reg.", "l1 reg.", "l2 reg.", "weight decay", "noise reg. (ours)",])

fig.tight_layout()
fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_GMM_Skew.png"))
fig.savefig(os.path.join(os.path.join(DATA_DIR_LOCAL, EXP_PREFIX), "regularization_comparison_GMM_Skew.pdf"))