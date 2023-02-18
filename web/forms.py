from django import forms
  
symbol_choices =(
    ("1", "model_dqn_GOOG_50"),
    ("2", "model_t-dqn_GOOG_10"),
    ("3", "model_double-dqn_GOOG_50"),
)
class webForm(forms.Form):
    options = forms.MultipleChoiceField(choices = symbol_choices)
