import os
import yaml
from tqdm import tqdm
import csv
import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument("--base_yaml_path", required=True)
    parser.add_argument("--save_prefix_path", default="seshat/")
    parser.add_argument("--gbd_testing", default= False)
    # parser.add_argument("--testing", default= True)
    return parser.parse_args()

def year_processing(year):
    if year < 0:
        return f"{year * -1} BCE"
    else:
        return f"{year} CE"
if __name__ == "__main__":
    args = parse_args()
    if args.gbd_testing:
        base_data_path = "/raid5pool/tank/hauser/tasks/seshat-benchmark"
    else:
        base_data_path = "/home/scrappy/csh/Hapi/data/seshat-benchmark"
    with open("lm_eval/tasks/seshat/polity_info.csv", "r") as csvfile:
        polity_reader = csv.reader(csvfile,delimiter="|",)
        id_index = 3
        name_index = 4
        macro_reg_index = 0
        reg_index = 1
        start_year_index = 5
        end_year_index = 6
        
        task_set = set()
        max_count = 0
        count = 0
        # if args.testing:
        #     max_count = 20
        for row in polity_reader:
            # count += 1
            # if count == max_count:
            #     break
            start_year = row[start_year_index]
            print(start_year)
            end_year = row[end_year_index]
            print(end_year)
            mean_year = int(start_year) + int(end_year) / 2
            year_basket = year_processing((mean_year // 100 ) * 100)
              
            task_type = "guess_value"
            file_path = f"{base_data_path}/guess_value/test_{row[id_index]}.parquet"
            if not os.path.exists(file_path) or "**" in row[id_index]:
                continue
            guess_value_abs_pres_dict = {
                "task" : f"{task_type}_{row[id_index]}",
                "dataset_path": "parquet",
                "dataset_kwargs" : {
                    "data_files" : {
                        # "test" : f"{base_data_path}/guess_value_abs_pres/test_{row[id_index]}.parquet"
                        "test" : file_path
                        }
                    },
                "metric_list": [{"metric" : "acc",
                                 "aggregation": "mean",
                                 "higher_is_better": "true"}],
                "output_type": "multiple_choice",
                "test_split": "test",
                "doc_to_text": "Q",
                "doc_to_target": "A",
                # "doc_to_choice": [ "absent", "present","inferred absent","inferred present"],
                "doc_to_choice": ["A","B","C","D"],
                # "group" : [row[macro_reg_index], row[reg_index], row[id_index]]
                "group" : [row[macro_reg_index], row[reg_index], row[id_index], year_basket]
                }
            task_set.add(row[macro_reg_index])
            # task_set.add(row[reg_index])
     

            save_path = args.save_prefix_path + f"{task_type}/{row[id_index]}.yaml"
            # print(save_path)

            with open(save_path, "w", encoding="utf-8") as yaml_file:
                yaml.dump(
                    guess_value_abs_pres_dict,
                    yaml_file,
                    allow_unicode=True,
                    default_style='"',
                )
            
            task_type = "extract_value"
            file_path = f"{base_data_path}/extract_value/test_{row[id_index]}.parquet"
            if not os.path.exists(file_path) or "**" in row[id_index]:
                continue
            guess_value_abs_pres_dict = {
                "task" : f"{task_type}_{row[id_index]}",
                "dataset_path": "parquet",
                "dataset_kwargs" : {
                    "data_files" : {
                        # "test" : f"{base_data_path}/guess_value_abs_pres/test_{row[id_index]}.parquet"
                        "test" : file_path
                        }
                    },
                "metric_list": [{"metric" : "acc",
                                 "aggregation": "mean",
                                 "higher_is_better": "true"}],
                "output_type": "multiple_choice",
                "test_split": "test",
                "doc_to_text": "Q",
                "doc_to_target": "A",
                # "doc_to_choice": [ "absent", "present","inferred absent","inferred present"],
                "doc_to_choice": ["A","B","C","D"],
                # "group" : [row[macro_reg_index], row[reg_index], row[id_index]]
                "group" : [row[macro_reg_index], row[reg_index], row[id_index], year_basket]
                # "group" : [row[macro_reg_index], row[id_index]]
                }
            task_set.add(row[macro_reg_index])
            # task_set.add(row[reg_index])
     

            save_path = args.save_prefix_path + f"{task_type}/{row[id_index]}.yaml"
            # print(save_path)

            with open(save_path, "w", encoding="utf-8") as yaml_file:
                yaml.dump(
                    guess_value_abs_pres_dict,
                    yaml_file,
                    allow_unicode=True,
                    default_style='"',
                )
            seshat_dict = {
                "group" : "seshat",
                "task" : list(task_set)
                }

            save_path = args.save_prefix_path + f"_seshat.yaml"
            # print(save_path)

            with open(save_path, "w", encoding="utf-8") as yaml_file:
                yaml.dump(
                    seshat_dict,
                    yaml_file,
                    allow_unicode=True,
                    default_style='"',
                )
