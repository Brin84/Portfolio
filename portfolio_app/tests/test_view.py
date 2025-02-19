import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.test import RequestFactory
from portfolio_app.models import Project
from portfolio_app.views import ProjectDetailView


@pytest.mark.django_db
class TestProjectDetailView:
    def setup_method(self):
        self.factory = RequestFactory()
        self.view = ProjectDetailView.as_view()
        self.project = Project.objects.create(title="Test Project", description="Test Description")
        self.url = reverse('portfolio_app:project_detail', kwargs={'pk': self.project.pk})
        self.redirect_url = reverse('portfolio_app:projects')

    def test_project_exists(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        assert "Test Project" in response.content.decode()
        assert "Test Description" in response.content.decode()

    def test_project_does_not_exist(self, client):
        nonexistent_url = reverse('portfolio_app:project_detail', kwargs={'pk': 2})
        response = client.get(nonexistent_url, follow=True)

        assert response.status_code == 200
        assert response.redirect_chain[0][0] == self.redirect_url
        messages = [msg.message for msg in get_messages(response.wsgi_request)]
        assert "На данный момент проектов нет." in messages

    def test_get_object_redirect(self):
        request = self.factory.get(self.url)
        request.user = None
        response = ProjectDetailView.as_view()(request, pk=19)

        assert response.status_code == 302
        assert response.url == self.redirect_url
