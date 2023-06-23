import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
from pprint import pprint
import zipfile

VERBOSE = False
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'container_test')
os.makedirs(TEMP_DIR, exist_ok=True)

TEST_LIST_PATH = '../../test_data/test_singularity.galaxyproject.org_list.txt'
TEST_JSON_PATH = '../../test_data/test_singularity.galaxyproject.org_images.json'
TEST_FILTERED_JSON_PATH = '../../test_data/test_filtered_singularity.galaxyproject.org_images.json'
TEST_DIR_ZIP_PATH = '../../test_data/test_singularity.galaxyproject.org.zip'
TEMP_IMAGE_DIR = os.path.join(TEMP_DIR, 'test_singularity.galaxyproject.org')
TEMP_JSON_PATH = os.path.join(TEMP_DIR, 'temp_singularity.galaxyproject.org_images.json')
TEST_RECORD = [
    'tool_name',
    'sortable_subversion_list',
    'image_build',
    'image_variant',
    'version_string',
    'variant_string',
    'image_bytes',
    'image_datetime',
    'image_path',
]

# We need to load the container script without the .py extension as a Python module
spec = spec_from_loader("container", SourceFileLoader("container", "../container"))
container = module_from_spec(spec)
spec.loader.exec_module(container)


class FakeArgs(object):
    """Fake arguments"""

    def __init__(self):
        self.quiet = True
        self.refresh = False
        self.version = None
        self.latest = False
        self.all = False
        self.modified = False
        self.size = False


class ContainerTestCase(unittest.TestCase):
    @staticmethod
    def compare_image_info_dicts_without_dates(image_info_dict1, image_info_dict2):
        """Need to ignore date modified for comparisons when listing real files because dates may change"""
        for tool_name, tool_values1 in image_info_dict1.items():
            if not (tool_values2 := image_info_dict2.get(tool_name)):
                return False
            for version, version_values1 in tool_values1.items():
                if not (version_values2 := tool_values2.get(version)):
                    return False
                for variant, variant_values1 in version_values1.items():
                    if not (variant_values2 := version_values2.get(variant)):
                        return False
                    if variant_values1[:2] != variant_values2[:2]:  # Don't look at third element (image_datetime)
                        return False
        return True

    @staticmethod
    def refresh_test_dir(zip_path, test_dir_path):
        if os.path.isdir(test_dir_path):
            shutil.rmtree(test_dir_path)
        zipped_test_dir = zipfile.ZipFile(zip_path)
        zipped_test_dir.extractall(path=os.path.dirname(test_dir_path))

    def test_parse_image_info(self):
        with open(TEST_LIST_PATH) as line_source:
            image_info_dict = container.parse_image_info(line_source)

        # with open(TEST_JSON_PATH, 'w') as json_file:
        #     json_file.write(json.dumps(image_info_dict))

        with open(TEST_JSON_PATH) as json_file:
            test_json_object = json.loads(json_file.read())

        self.assertEqual(image_info_dict, test_json_object)

    def test_get_image_info_from_cache(self):
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.refresh = False

        image_info_dict = container.get_image_info(cache_json_path=TEST_JSON_PATH,
                                                   image_dir='blah',
                                                   list_url='blah',
                                                   min_cache_datetime=datetime(2000, 1, 1, 0, 0, 0, 0),  # Never expire
                                                   args=args)

        with open(TEST_JSON_PATH) as json_file:
            test_json_object = json.loads(json_file.read())

        self.assertEqual(image_info_dict, test_json_object)

    def test_get_image_info_from_dir_expired_cache(self):

        if os.name != 'posix':
            print("Skipping directory listing test in non-posix OS")
            return

        self.refresh_test_dir(TEST_DIR_ZIP_PATH, TEMP_IMAGE_DIR)

        args = FakeArgs()
        args.quiet = not VERBOSE
        args.refresh = False

        image_info_dict = container.get_image_info(cache_json_path=TEMP_JSON_PATH,
                                                   image_dir=TEMP_IMAGE_DIR,
                                                   list_url='blah',
                                                   min_cache_datetime=datetime.now(),  # Always expire cache
                                                   args=args)

        with open(TEST_JSON_PATH) as json_file:
            test_json_object = json.loads(json_file.read())

        self.assertTrue(self.compare_image_info_dicts_without_dates(image_info_dict, test_json_object))

    def test_get_image_info_from_dir_forced_refresh(self):

        if os.name != 'posix':
            print("Skipping directory listing test in non-posix OS")
            return

        self.refresh_test_dir(TEST_DIR_ZIP_PATH, TEMP_IMAGE_DIR)

        args = FakeArgs()
        args.quiet = not VERBOSE
        args.refresh = True

        image_info_dict = container.get_image_info(cache_json_path=TEMP_JSON_PATH,
                                                   image_dir=TEMP_IMAGE_DIR,
                                                   list_url=container.LIST_URL,
                                                   min_cache_datetime=datetime(2000, 1, 1, 0, 0, 0, 0),  # Never expire
                                                   args=args)

        with open(TEST_JSON_PATH) as json_file:
            test_json_object = json.loads(json_file.read())

        self.assertTrue(self.compare_image_info_dicts_without_dates(image_info_dict, test_json_object))

    def test_get_image_info_from_url_expired_cache(self):
        """This is a bit of a rubbish test which checks the URL"""
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.refresh = False

        try:
            os.remove(TEMP_JSON_PATH, )
        except FileNotFoundError:
            pass

        image_info_dict = container.get_image_info(cache_json_path=TEMP_JSON_PATH,
                                                   image_dir=TEMP_IMAGE_DIR,
                                                   list_url=container.LIST_URL,
                                                   min_cache_datetime=datetime.now(),  # Always expire cache
                                                   args=args)

        self.assertTrue(len(image_info_dict) > 10000)

    def test_get_sort_function_default_sort(self):
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.modified = False
        args.size = False
        sort_function = container.get_sort_function(args)
        self.assertEqual(sort_function(TEST_RECORD), ('tool_name', 'sortable_subversion_list', 'image_build'))

    def test_get_sort_function_modified_sort(self):
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.modified = True
        args.size = False
        sort_function = container.get_sort_function(args)
        self.assertEqual(sort_function(TEST_RECORD), ('tool_name', 'image_datetime'))

    def test_get_sort_function_size_sort(self):
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.modified = False
        args.size = True
        sort_function = container.get_sort_function(args)
        self.assertEqual(sort_function(TEST_RECORD), ('tool_name', 'image_bytes'))

    def test_filter_image_info(self):
        with open(TEST_JSON_PATH) as json_file:
            image_info_dict = json.loads(json_file.read())

        tool_search_strings = ['samtools']

        filtered_image_info = container.filter_image_info(image_info_dict, tool_search_strings)

        with open(TEST_FILTERED_JSON_PATH) as json_file:
            test_json_object = json.loads(json_file.read())

        self.assertEqual(filtered_image_info, test_json_object)

    def test_make_sortable_list_by_version(self):
        args = FakeArgs()
        args.quiet = not VERBOSE
        args.modified = False
        args.size = False
        args.version = '1.2'

        with open(TEST_FILTERED_JSON_PATH) as json_file:
            result_info_dict = json.loads(json_file.read())

        sort_function = container.get_sort_function(args)

        sortable_list = container.make_sortable_list(result_info_dict, sort_function, args)

        expected_result = [
            ('samtools',
             ['0000000001', '0000000002'],
             0,
             '',
             '1.2',
             '',
             '5',
             '2023-06-23T10:08:04',
             '/cvmfs/singularity.galaxyproject.org/all/samtools:1.2'),
            ('samtools',
             ['0000000001', '0000000002'],
             0,
             '',
             '1.2',
             '0',
             '5',
             '2023-06-23T10:08:04',
             '/cvmfs/singularity.galaxyproject.org/all/samtools:1.2-0'),
            ('samtools',
             ['0000000001', '0000000002', 'rglab'],
             0,
             '',
             '1.2.rglab',
             '0',
             '5',
             '2023-06-23T10:08:04',
             '/cvmfs/singularity.galaxyproject.org/all/samtools:1.2.rglab--0')
        ]

        self.assertEqual(sortable_list, expected_result)


if __name__ == '__main__':
    unittest.main()
