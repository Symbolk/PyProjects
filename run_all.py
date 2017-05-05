from Utils.join_prob import *
from XGBoost_expr.main import *
from XGBoost_var.main import *
from XGBoost_expr.gen_exprs import *
from Utils.predict_vars import *


if __name__ == '__main__':
    params ={
        'project':'fastjson',
        'bugid':'',
        'type': 'expr',
        'expr_frequency': 1,
        'model_path': 'model/',
        'input_path':'input/',
        'output_path':'output/',
        'gen_expr_top': 10
    }
    # run_expr(params)
    # run_var(params)
    # run_predict_vars(params)
    # run_gen_exprs(params)
    # join_prob(params)
