# Predicate Suggester

---

**A code hinting model focusing on predicates(if/for/while) in codes.**

_Powered By [@Symbolk](http://www.symbolk.com)_

Language:

> Python

Based on:

> [XGBoost](https://github.com/dmlc/xgboost)

IDE:

> Pycharm(http://www.jetbrains.com/pycharm/)

---

## Usage

1, Install XGBoost with all its dependencies(e.g. scipy, numpy, matplotlib, pandas...);

2, Config the run_all.py according the use case, e.g.:

```python


if __name__ == '__main__':
    params ={
        'project':'RxJava',
        'bugid':'',
        'type': 'expr',
        'expr_frequency': 1,
        'model_path': 'model/',
        'input_path':'input/',
        'output_path':'output/',
        'gen_expr_top': 20
    }
    run_expr(params)
    run_var(params)
    run_predict_vars(params)
    run_gen_exprs(params)
    join_prob(params)

}
```

3, Run the run_all.py in shell or in Pycharm, see console for outputs.
