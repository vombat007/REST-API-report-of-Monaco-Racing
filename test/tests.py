import pytest
from pathlib import Path
from bin.web_app import sort_asc_desc, app


class TestClass:
    def test_sort_asc(self):
        result = sort_asc_desc(Path.cwd() / app.config.get('STATIC_FOLDER'), 'asc')
        assert result['SVF'] == {
            'name': 'Sebastian Vettel',
            'place': '1',
            'team': 'FERRARI',
            'time': '1:04.415'
                                 }

    def test_report_asc(self):
        response = app.test_client().get('/api/v1/report/?format=json&order=asc')
        assert {'name': 'Charles Leclerc',
                'place': '6',
                'team': 'SAUBER FERRARI',
                'time': '1:12.829'} == response.get_json()['CLS']

    def test_report_desc(self):
        response = app.test_client().get('/api/v1/report/?format=json&order=desc')
        assert {'name': 'Sebastian Vettel',
                'place': '1',
                'team': 'FERRARI',
                'time': '1:04.415'} == response.get_json()['SVF']

    def test_driver_id(self):
        response = app.test_client().get('/api/v1/report/DRR/')
        assert {'response': {'name': 'Daniel Ricciardo',
                             'place': '16',
                             'team': 'RED BULL RACING TAG HEUER',
                             'time': 'Error time'}} == response.get_json()




    def test_report_asc_xml(self):
        response = app.test_client().get('/api/v1/report/?format=xml&order=asc')
        assert 'f' == response.get_data()

