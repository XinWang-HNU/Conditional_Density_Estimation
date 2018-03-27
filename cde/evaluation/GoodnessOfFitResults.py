import pandas as pd
import traceback
from cde.utils import io

class GoodnessOfFitResults:
  def __init__(self, single_results_list):
    assert len(single_results_list) > 0, "given single results list is empty"

    self.single_results = single_results_list
    self.results_df = None



  def __len__(self):
    return 1

  def generate_results_dataframe(self, keys_of_interest):
    dfs = []
    for single_result in self.single_results:
      dfs.append(pd.DataFrame(single_result.report_dict(keys_of_interest=keys_of_interest)))

    self.results_df = pd.concat(dfs, axis=0).reindex_axis(keys_of_interest, axis=1)
    #self.results_df = self.results_df.reindex(columns=keys_of_interest)
    return self.results_df


  def export_results_as_csv(self, keys_of_interest, output_dir, file_name):
    if self.results_df is None:
      self.generate_results_dataframe(keys_of_interest=keys_of_interest)

    file_results = io.get_full_path(output_dir=output_dir, suffix=".csv", file_name=file_name)
    file_handle_results_csv = open(file_results, "w+")

    """ write result to file"""
    try:
      io.append_result_to_csv(file_handle_results_csv, self.results_df)
    except Exception as e:
      print("exporting results as csv was not successful")
      print(str(e))
      traceback.print_exc()
    finally:
      file_handle_results_csv.close()

  def plot_metric(self, graph_dicts, metric='hellinger_distance', simulator='EconDensity'):
    assert self.results_df is not None, "first generate results df"
    assert simulator in list(self.results_df["simulator"]), simulator + " not in the results dataframe"
    assert metric in self.results_df


    for graph_dict in graph_dicts:
      n_obs = self.results_df.loc["estimator" == graph_dict["estimator"]]


    raise NotImplementedError