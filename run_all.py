from XGBoost_expr.main import *
from Utils.predict_vars import *
from Utils.gen_exprs import *
from XGBoost_var.main import *


if __name__ == '__main__':
    params ={
        'project':'chart',
        'bugid':'1',
        'type': 'expr',
        'expr_frequency': 10,
        'model_path': 'model/',
        'input_path':'input/',
        'output_path':'output/'
    }
    run_expr(params)
    # run_var(params)
    # run_predict_vars(params)
    # run_gen_exprs(params)
