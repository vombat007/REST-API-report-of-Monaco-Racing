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

    def test_driver_id(self):
        response = app.test_client().get('/api/v1/report/DRR/')
        assert b"16" in response.data
        assert b"Daniel Ricciardo" in response.data
        assert b"RED BULL RACING TAG HEUER" in response.data
        assert b"Error time" in response.data

    def test_order(self):
        response = app.test_client().get('/api/v1/report/order/')
        assert b"18" in response.data
        assert b"Esteban Ocon" in response.data
        assert b"FORCE INDIA MERCEDES" in response.data
        assert b"Error time" in response.data
