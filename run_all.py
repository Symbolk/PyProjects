from Utils.join_prob import *
from XGBoost_expr.main import *
from XGBoost_expr.gen_exprs import *


if __name__ == '__main__':
    params ={
        'project':'math',
        'bugid':'3',
        'type': 'expr',
        'expr_frequency': 10,
        'model_path': 'model/',
        'input_path':'input/',
        'output_path':'output/',
        'gen_expr_top': 10
    }
    # run_expr(params)
    # run_var(params)
    # run_predict_vars(params)
    run_gen_exprs(params)
    # join_prob(params)
