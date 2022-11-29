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

    def test_none_index_route(self):
        response = app.test_client().get('/none')
        assert response.status_code == 404

    def test_report_route(self):
        response = app.test_client().get('/api/v1/report/?format=json')
        assert response.status_code == 200

    def test_driver_id_route(self):
        response = app.test_client().get('/api/v1/report/DRR/')
        assert response.status_code == 200

    def test_order_route(self):
        response = app.test_client().get('/api/v1/report/order/')
        assert response.status_code == 200

