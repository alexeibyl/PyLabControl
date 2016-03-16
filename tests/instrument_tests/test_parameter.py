from unittest import TestCase
from copy import deepcopy
from src.core.instruments import Parameter, get_elemet

class TestParameter(TestCase):

    def Ttest_init(self):
        # initiate Paremater in all possible ways
        p1 = Parameter('param1', 0.0)
        p2 = Parameter('param2', 0, int, 'test int')
        p3 = Parameter('param3', 0.0, float, 'test tupple')
        p4 = Parameter('param4', 0.0, [0.0, 0.1], 'test list')

        p4.value = 0.1
        p1.value = '1e6'
        p1.value = '13'
        p2.value = 0.1
        p2.value = '13'
        with self.assertRaises(ValueError):
            p4.value = 0.2
            p2.value = 's'


        print(p1.as_dict())
        print(p2.as_dict())
        print(p3.as_dict())
        print(p4.as_dict())

        p_nested = Parameter('param nested', p1, None, 'test list')
        p_nested = Parameter('param nested', p4, [p1,p4], 'test list')

        p_dict = Parameter({'param dict': 0 })
        p_dict_nested = Parameter({'param dict': {'sub param dict': 1 } })

    def Ttest_update_Parameter(self):

        # ======================================================
        # update Parameter
        p1 = Parameter('param', 0)
        p1.value = 0.1
        p1.value = '2'
        p1 = Parameter('par 3', [1,2])
        new_value = [2,3,5,4]
        p1.value = new_value
        self.assertEquals(new_value, p1.value)

        # ======================================================
        p1 = Parameter('param', 0)
        p1b = Parameter('param', 1)
        p2 = Parameter('param2', 2)
        p3 = Parameter('par 3', [p1, p2])
        p4 = Parameter('param4', 4)


        # ======================================================
        p3 = Parameter('par 3', [p1, p2])
        initial = deepcopy(p3.as_dict())
        p3.value = p1
        final = p3.as_dict()

        self.assertEquals(initial, final)

        # ======================================================
        # this should give an IndexError
        p3 = Parameter('par 3', [p1, p2])
        with self.assertRaises(IndexError):
            p3.value = [p4,p1]
        # p3.value = p1

        # ======================================================
        # if value is a parameter, the is should also be able to accept dictionaries and cast them into parameter objects
        p1 = Parameter('param', 0)
        p2 = Parameter('param2', p1)
        p2.value = Parameter('param', 4)

        # p2.value = {'param' : 4}


    def test_casting(self):
        '''
        test all possible ways to update a parameter
        :return:
        '''
        p1 = Parameter('param', 0)
        p2 = Parameter('param2', 2)
        p3 = Parameter('param3', [p1, p2])

        print(p1['param'])
        p1['param'] = 44

        #
        # initial = deepcopy(p3.as_dict())
        # p3.value = Parameter({'param2': 4})
        # final = deepcopy(p3.as_dict())
        #
        # get_elemet('param', p3.value).value = 3
        #
        # # print(p1.as_dict())
        # # print(p3.as_dict())
        # # print(p3)
        #
        # parameters = {'param1': 'value1', 'param2': 'value2'}
        # parameters = [{'param1':'value1'}, {'param2':'value2'}]
        # parameters = [Parameter('param1', 'value1'), Parameter('param2', 'value2')]
        # print(p1.as_dict())

        print(p1.as_dict())