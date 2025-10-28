import shap

def shap_summary(model, X):
    explainer = shap.TreeExplainer(model)
    return explainer.shap_values(X)
