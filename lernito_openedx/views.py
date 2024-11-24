import logging
import hmac
import hashlib
import json
from typing import Dict, Any
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.djangoapps.student.models import CourseEnrollment, UserProfile
from common.djangoapps.student.models import CourseEnrollmentAllowed
from django.contrib.auth.models import User
from .serializers import LernitoWebhookSerializer

logger = logging.getLogger(__name__)

class LernitoWebhookView(APIView):
    """
    API View for handling Lernito webhooks.
    Processes user enrollment requests from Lernito service.
    """
    
    def validate_webhook_signature(self, data: Dict[str, Any], headers: Dict[str, str]) -> bool:
        """
        Validate the webhook signature using HMAC
        
        The signature is expected to be in the X-Lernito-Signature header
        The signature is a HMAC SHA256 hash of the request data using the webhook secret
        """
        signature = headers.get('X-Lernito-Signature')
        if not signature:
            return False

        webhook_secret = getattr(settings, 'LERNITO_WEBHOOK_SECRET', None)
        if not webhook_secret:
            logger.error('LERNITO_WEBHOOK_SECRET not configured in settings')
            return False

        # Convert the data back to a consistent string format for hashing
        data_string = json.dumps(data, sort_keys=True)
        
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            data_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to the webhook endpoint
        """
        # Verify webhook signature using the parsed data
        if not self.validate_webhook_signature(request.data, request.headers):
            return Response({
                'success': False,
                'message': 'Invalid signature'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Validate payload using serializer
            serializer = LernitoWebhookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract validated data
            validated_data = serializer.validated_data
            email = validated_data['email']
            name = validated_data['name']
            family = validated_data['family']
            username = validated_data['username']
            course_ids = validated_data['courseIds']
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                # User exists, directly enroll them in all courses
                for course_id in course_ids:
                    enrollment = CourseEnrollment.enroll(user, course_id)
                message = f'User enrolled successfully in {len(course_ids)} course(s)'
            except User.DoesNotExist:
                # User doesn't exist, create enrollment allowed for all courses
                for course_id in course_ids:
                    CourseEnrollmentAllowed.objects.create(
                        email=email,
                        course_id=course_id,
                        auto_enroll=True
                    )
                message = f'Enrollment allowed created successfully for {len(course_ids)} course(s)'
            
            # Log the successful operation
            logger.info(
                f"Lernito webhook processed successfully for email: {email}, "
                f"name: {name} {family}, "
                f"course_ids: {course_ids}"
            )
            
            return Response({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            logger.error(f"Error processing Lernito webhook: {str(e)}")
            return Response({
                'success': False,
                'message': 'Internal server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Use this payload to test the webhook
# {"email": "test@example.com", "name": "Test", "family": "User", "username": "testuser", "courseIds": ["course-v1:edX+DemoX+Demo_Course"]}
# The signature is a HMAC SHA256 hash of the request data using the webhook secret
# X-Lernito-Signature: 0a48a78817b613abdc3d094ca2a7ba59bddfe6d5535c99a00eefc73a6b26e64f