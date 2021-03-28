import pytest
import unittest
from src.gmaillabelcreate.gmaillabel import (define_label, VALUE_ERROR_DEFINE_LABEL_TEXT,
VALUE_ERROR_DEFINE_LABEL_COLOR_TEXT)

def test_define_label():
    color_dict = {
        'pending':{'textColor': '#ffffff', 'backgroundColor': '#c2c2c2'},
        }

    correct_out = {
        "name": "test",
        "color": color_dict['pending'],
        "messageListVisibility": "mlv",
        "labelListVisibility": "llv",
        "type": "tp" 
        }

    assert correct_out == define_label("test", color=color_dict['pending'], mlv="mlv", llv="llv", tp="tp")

class TestDefineLabelValues:

    @pytest.mark.parametrize("args, excpected_output",[
        ((1, True, 1.1, None, (1), [1], {1:1}), (VALUE_ERROR_DEFINE_LABEL_TEXT.format(["name"]))),
    ])
    def test_args_values(self, args, excpected_output):
        # tests to check 'name' argument
        for arg in args:
            with pytest.raises(ValueError) as exec_info:
                define_label(arg)
            assert str(exec_info.value) == excpected_output
    
    @pytest.mark.parametrize("kwargs, excpected_output",[
        (({"mlv":1}, {"mlv":True}, {"mlv":1.1}, {"mlv":None}, {"mlv":(1)}, {"mlv":[1]}, {"mlv":{1:1}}), (VALUE_ERROR_DEFINE_LABEL_TEXT.format(["mlv"]))),
        (({"llv":1}, {"llv":True}, {"llv":1.1}, {"llv":None}, {"llv":(1)}, {"llv":[1]}, {"llv":{1:1}}), (VALUE_ERROR_DEFINE_LABEL_TEXT.format(["llv"]))),
        (({"tp":1}, {"tp":True}, {"tp":1.1}, {"tp":None}, {"tp":(1)}, {"tp":[1]}, {"tp":{1:1}}), (VALUE_ERROR_DEFINE_LABEL_TEXT.format(["tp"]))),
        (({"color":{"test":1, "textColor":"#ffffff"}},), (VALUE_ERROR_DEFINE_LABEL_COLOR_TEXT.format(["backgroundColor"]))),
        (({"color":{"test":1, "backgroundColor":"#ffffff"}},), (VALUE_ERROR_DEFINE_LABEL_COLOR_TEXT.format(["textColor"]))),
    ])
    def test_kwargs_values(self, kwargs, excpected_output):
        # tests to check 'name' argument
        for kwarg in kwargs:
            with pytest.raises(ValueError) as exec_info:
                define_label("test_name", **kwarg)
            assert str(exec_info.value) == excpected_output
