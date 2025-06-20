"""
Middleware для интеграции с Sentry.
"""

import sentry_sdk
from typing import Any, Callable
from django.http import HttpRequest, HttpResponse


class SentryMiddleware:
    """
    Middleware для автоматического отслеживания пользователей и контекста в Sentry.
    """
    
    def __init__(self, get_response: Callable) -> None:
        """
        Инициализация middleware.
        
        Args:
            get_response: Функция для получения ответа.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Обработка запроса.
        
        Args:
            request: HTTP запрос.
            
        Returns:
            HTTP ответ.
        """
        # Устанавливаем контекст пользователя, если он аутентифицирован
        if hasattr(request, 'user') and request.user.is_authenticated:
            sentry_sdk.set_user({
                "id": request.user.id,
                "username": request.user.username,
                "email": getattr(request.user, 'email', None),
            })
        
        # Устанавливаем контекст запроса
        sentry_sdk.set_context("request", {
            "method": request.method,
            "path": request.path,
            "user_agent": request.META.get('HTTP_USER_AGENT', 'Unknown'),
            "remote_addr": request.META.get('REMOTE_ADDR', 'Unknown'),
        })
        
        # Устанавливаем теги для группировки событий
        sentry_sdk.set_tag("method", request.method)
        
        response = self.get_response(request)
        
        # Добавляем информацию о статусе ответа
        sentry_sdk.set_tag("status_code", response.status_code)
        
        return response 