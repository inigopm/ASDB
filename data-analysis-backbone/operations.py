import sys
import runpy
from memory_profiler import profile

PATH = "./scripts/"
PATH_ANALYITCAL_SANDBOX = PATH + "analytical-sandbox/"
PATH_FEATURE_GENERATION = PATH + "feature-generation/"
# {
PATH_DATA_PREPARATION = "data-preparation/"
PATH_FEATURE_SELECTION = "feature-selection/"
PATH_LABELLING = "labelling/"
PATH_TRAIN_TEST_SPLIT = "train-test-split/"
# }
PATH_MODEL_TRAINING = PATH + "model-training/"
PATH_MODEL_VALIDATION = PATH + "model-validation/"

# @profile
def main():
    print("Running ANALYITCAL-SANDBOX")
    runpy.run_path(PATH_ANALYITCAL_SANDBOX + 'articles_with_prices.py')
    runpy.run_path(PATH_ANALYITCAL_SANDBOX + 'daily_metrics.py')

    print("Running FEATURE-GENERATION")
    runpy.run_path(PATH_FEATURE_GENERATION + PATH_DATA_PREPARATION + "regression_model.py")
    runpy.run_path(PATH_FEATURE_GENERATION + PATH_DATA_PREPARATION + "pca.py")

    runpy.run_path(PATH_FEATURE_GENERATION + PATH_FEATURE_SELECTION + "pca.py")

    runpy.run_path(PATH_FEATURE_GENERATION + PATH_LABELLING + "regression_model.py")

    runpy.run_path(PATH_FEATURE_GENERATION + PATH_TRAIN_TEST_SPLIT + "train_test_split.py")
    
    print("Running MODEL-TRAINING")
    runpy.run_path(PATH_MODEL_TRAINING + "regression_model_training.py")

    print("Running MODEL-VALIDATION")
    runpy.run_path(PATH_MODEL_VALIDATION + "regression_model.py")

    print("The Data Analysis Pipeline run successfully")
    

main()
