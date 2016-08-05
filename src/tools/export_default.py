"""
    This file is part of PyLabControl, software for laboratory equipment control for scientific experiments.
    Copyright (C) <2016>  Arthur Safira, Jan Gieseler, Aaron Kabcenell

    Foobar is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
# from importlib import import_module
from PyLabControl.src.core.read_write_functions import get_config_value
import inspect, os
from PyLabControl.src.core import Instrument, Script
from importlib import import_module
from PyLabControl.src.core.helper_functions import module_name_from_path

def get_classes_in_folder( folder_name, class_type):
    """
    load all the instruments objects that are located in folder_name and
    return a dictionary with the script class name and path_to_python_file
    Args:
        folder_name (string): folder in which to search for class objects / or name of module
        class_type (string or class): class type for which to look for

    Returns:
        a dictionary with the class name and path_to_python_file:
        {
        'class': class_of_instruments,
        'filepath': path_to_python_file
        }

    """

    assert class_type == Instrument or class_type == Script or class_type.lower() in ['instrument', 'script']

    if isinstance(class_type, str):
        if class_type.lower() == 'instrument':
            class_type = Instrument
        elif class_type.lower() == 'script':
            class_type = Script


    # if the module name was passed instead of a filename, figure out the path to the module
    if not os.path.isdir(folder_name):
        try:
            folder_name = os.path.dirname(inspect.getfile(import_module(folder_name)))
        except ImportError:
            raise ImportError('could not find module ' + folder_name)

    subdirs = [os.path.join(folder_name, x) for x in os.listdir(folder_name) if
               os.path.isdir(os.path.join(folder_name, x)) and not x.startswith('.')]

    classes_dict = {}

    if len(subdirs) > 0:
        # if there are subdirs in the folder recursively check all the subfolders for scripts
        # skip the first one since this is the main folder
        for subdir in subdirs:
            print('subdir', subdir, class_type)
            classes_dict.update(get_classes_in_folder(subdir, class_type))


    print('folder_name', folder_name)
    module, path = module_name_from_path(folder_name)
    print('module, path', module, path)
    module = import_module(module)

    classes_dict.update({name: {'class': name, 'filepath': inspect.getfile(obj)} for name, obj in
                           inspect.getmembers(module) if inspect.isclass(obj) and issubclass(obj, class_type)})
    return classes_dict

# def get_instruments_in_path(folder_name):
#     """
#     load all the instruments objects that are located in folder_name and
#     return a dictionary with the script class name and path_to_python_file
#     Args:
#         folder_name: folder in which to search for instruments objects / or name of module
#
#     Returns:
#         a dictionary with the instruments class name and path_to_python_file:
#         {
#         'class': class_of_instruments,
#         'filepath': path_to_python_file
#         }
#
#     """
#
#     # if the module name was passed instead of a filename, figure out the path to the module
#     if not os.path.isdir(folder_name):
#         try:
#             folder_name = os.path.dirname(inspect.getfile(import_module(folder_name)))
#         except ImportError:
#             raise ImportError('could not find module ' + folder_name)
#
#     subdirs = [os.path.join(folder_name, x) for x in os.listdir(folder_name) if
#                os.path.isdir(os.path.join(folder_name, x)) and not x.startswith('.')]
#     instruments_to_load = {}
#
#     if len(subdirs) > 0:
#         # if there are subdirs in the folder recursively check all the subfolders for scripts
#         # skip the first one since this is the main folder
#         for subdir in subdirs:
#             instruments_to_load.update(get_instruments_in_path(subdir))
#
#     module, path = module_name_from_path(folder_name)
#     module = import_module(module)
#
#     instruments_to_load.update({name: {'class': name, 'filepath': inspect.getfile(obj)} for name, obj in
#                            inspect.getmembers(module) if inspect.isclass(obj) and issubclass(obj, Instrument)})
#     return instruments_to_load
#
#
# def get_scripts_in_path(folder_name):
#     """
#     load all the script objects that are located in folder_name and
#     return a dictionary with the script class name and path_to_python_file
#     Args:
#         folder_name: folder in which to search for script objects / or name of module
#
#     Returns:
#         a dictionary with the script class name and path_to_python_file:
#         {
#         'class': class_of_script,
#         'filepath': path_to_python_file
#         }
#
#     """
#
#     # if the module name was passed instead of a filename, figure out the path to the module
#     if not os.path.isdir(folder_name):
#         try:
#             folder_name = os.path.dirname(inspect.getfile(import_module(folder_name)))
#         except ImportError:
#             raise ImportError('could not find module ' + folder_name)
#
#     subdirs = [os.path.join(folder_name, x) for x in os.listdir(folder_name) if
#                os.path.isdir(os.path.join(folder_name, x)) and not x.startswith('.')]
#
#     scripts_to_load = {}
#     if len(subdirs) > 0:
#         # if there are subdirs in the folder recursively check all the subfolders for scripts
#         # skip the first one since this is the main folder
#         for subdir in subdirs:
#             scripts_to_load.update(get_scripts_in_path(subdir))
#
#     module, path = module_name_from_path(folder_name)
#
#     module = import_module(module)
#
#     scripts_to_load.update({name: {'class': name, 'filepath': inspect.getfile(obj)} for name, obj in
#                             inspect.getmembers(module) if inspect.isclass(obj) and issubclass(obj, Script)})
#
#     return scripts_to_load


def export_default_probes(path, module_name = ''):
    """
    NOT IMPLEMENTED YET
    tries to instantiate all the instruments that are imported in /instruments/__init__.py
    and the probes of each instrument that could be instantiated into a .b26 file in the folder path
    Args:
        path: target path for .b26 files
    """

    raise NotImplementedError


    import b26_toolkit.src.instruments as instruments
    from PyLabControl.src.core import Probe

    for name, obj in inspect.getmembers(instruments):

        if inspect.isclass(obj):

            try:
                instrument = obj()
                print('--- created ', obj.__name__, ' -- ')
                for probe_name, probe_info in instrument._PROBES.iteritems():
                    probe = Probe(instrument, probe_name, info = probe_info)
                    filename = os.path.join(path, '{:s}.b26'.format(instrument.name))
                    probe.save(filename)
            except:
                print('failed to create probe file for: {:s}'.format(obj.__name__))

def export_default_instruments(target_folder, source_folder = None, raise_errors = False):
    """
    tries to instantiate all the instruments that are imported in /instruments/__init__.py
    and saves instruments that could be instantiate into a .b2 file in the folder path
    Args:
        target_folder: target path for .b26 files
    """

    loaded_instruments = {}

    print('ffff', target_folder, source_folder)
    instruments_to_load = get_classes_in_folder(source_folder, Instrument)

    print('attempt to load {:d} instruments: '.format(len(instruments_to_load)))
    loaded_instruments, failed = Instrument.load_and_append(instruments_to_load)

    for name, value in loaded_instruments.iteritems():
        filename = '{:s}{:s}.b26'.format(target_folder, name)
        value.save_b26(filename)
        print('saving ', filename)

    print('\n================================================')
    print('================================================')
    print('saved {:d} instruments, {:d} failed'.format(len(loaded_instruments), len(failed)))
    if failed != {}:
        for error_name, error in failed.iteritems():
            print('failed to create instruments: ', error_name, error)

def export_default_scripts(target_folder, source_folder = None, raise_errors = False):
    """
    tries to instantiate all the scripts that are imported in /scripts/__init__.py
    saves each script that could be instantiated into a .b26 file in the folder path
    Args:
        target_folder: target path for .b26 files
        source_folder: location of python script files
    """
    loaded_instruments = {}
    loaded_scripts = {}


    scripts_to_load = get_classes_in_folder(source_folder, Script)

    print('attempt to load {:d} scripts: '.format(len(scripts_to_load)))
    loaded_scripts, failed, loaded_instruments = Script.load_and_append(scripts_to_load)

    for name, value in loaded_scripts.iteritems():
        filename = '{:s}{:s}.b26'.format(target_folder, name)
        value.save_b26(filename)
        print('saving ', filename)

    print('\n================================================')
    print('================================================')
    print('saved {:d} scripts, {:d} failed'.format(len(loaded_scripts), len(failed)))
    if failed != {}:
        for error_name, error in failed.iteritems():
            print('failed to create script: ', error_name, error)


#TODO: AK @ JG: is this as source_folder correct? Seems to fail if given a folder and not a name
def export(target_folder, source_folders = None, class_type ='all', raise_errors = False):
    """
    exports the existing scripts/intruments (future: probes) into folder as .b26 files
    Args:
        target_folder: target location of created .b26 script files
        source_folder: location of python script files or a list of folders
        class_type: string, one of the 4 following options
            -probes (exports probes) --not implemented yet--
            -scripts (exports scripts)
            -instruments (exports instruments)
            -all (exports instruments, scripts and probes)
        target_folder: target folder where .b26 files are created
    Returns:

    """
    if not class_type in ('all', 'scripts', 'instruments', 'probes'):
        print('unknown type to export')
        return


    if source_folders is None:
        module_list = [os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe())))]
    elif isinstance(source_folders, str):
        module_list = [source_folders]
    elif isinstance(source_folders, list):
        module_list = source_folders
    else:
        raise TypeError('unknown type for source_folders')

    print('aaa', module_list)
    for path_to_module in module_list:
        if class_type in ('all', 'scripts'):
            export_default_scripts(target_folder, source_folder=path_to_module, raise_errors=raise_errors)
        if class_type in ('all', 'instruments'):
            export_default_instruments(target_folder, path_to_module, raise_errors)
        if class_type in ('all', 'probes'):
            export_default_probes(target_folder, path_to_module, raise_errors)


if __name__ == '__main__':
    source_folder = 'C:/Users/Experiment/PycharmProjects/PyLabControl/src/'
    instruments_to_load = get_classes_in_folder(source_folder, Instrument)



    # source_folders = 'b26_toolkit'
    # target_folder = 'C:\\Users\\Experiment\\PycharmProjects\\user_data\\instruments_auto_generated'
    # export(target_folder, source_folders=None, class_type='instruments', raise_errors=False)

    # from PyLabControl.src.core import Script, Instrument
    # folder_name = 'b26_toolkit'
    # folder_name = '/Users/rettentulla/Projects/Python/b26_toolkit/src/'
    # # folder_name = '/Users/rettentulla/Projects/Python/PyLabControl/src/'
    # x = get_instruments_in_path(folder_name)
    # print(x.keys())
    # # for k, v in x.iteritems():
    # #     print(k, issubclass(v['x'], Script), issubclass(v['x'], Instrument))


    # folder_name = 'b26_toolkit'
    # # folder_name = '/Users/rettentulla/Projects/Python/b26_toolkit/'
    # # folder_name = '/Users/rettentulla/Projects/Python/PyLabControl/src/'
    # # x = get_classes_in_folder(folder_name, Script)
    # x = get_classes_in_folder(folder_name, 'script')
    # print(x.keys(), len(x.keys()))









