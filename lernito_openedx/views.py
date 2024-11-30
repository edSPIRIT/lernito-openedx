import hashlib
import hmac
import json
import logging
from typing import Any, Dict

from common.djangoapps.student.models import CourseEnrollment, CourseEnrollmentAllowed
from django.conf import settings
from django.contrib.auth.models import User
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LernitoWebhookSerializer

logger = logging.getLogger(__name__)


class LernitoWebhookView(APIView):
    """
    API View for handling Lernito webhooks.
    Processes user enrollment requests from Lernito service.
    """

    def validate_webhook_signature(
        self, data: Dict[str, Any], headers: Dict[str, str]
    ) -> bool:
        """
        Validate the webhook signature using HMAC

        The signature is expected to be in the X-Lernito-Signature header
        The signature is a HMAC SHA256 hash of the request data using the webhook secret
        """
        signature = headers.get("X-Lernito-Signature")
        if not signature:
            return False

        webhook_secret = getattr(settings, "LERNITO_WEBHOOK_SECRET", None)
        if not webhook_secret:
            logger.error("LERNITO_WEBHOOK_SECRET not configured in settings")
            return False

        # Convert the data back to a consistent string format for hashing
        # Remove spaces between json key values to ensure consistent hashing
        data_string = json.dumps(data, sort_keys=True, separators=(",", ":"))

        expected_signature = hmac.new(
            webhook_secret.encode("utf-8"), data_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()


        return hmac.compare_digest(signature, expected_signature)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to the webhook endpoint
        """
        # Verify webhook signature using the parsed data
        if not self.validate_webhook_signature(request.data, request.headers):
            return Response(
                {"success": False, "message": "Invalid signature"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # Validate payload using serializer
            serializer = LernitoWebhookSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(
                    {"success": False, "message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Extract validated data
            validated_data = serializer.validated_data
            email = validated_data["email"]
            name = validated_data["name"]
            family = validated_data["family"]
            username = validated_data["username"]
            course_ids = validated_data["courseIds"]

            # Check if Course Exists
            for course_id in course_ids:
                try:
                    course_key = CourseKey.from_string(course_id)
                    if not CourseOverview.objects.filter(id=course_key).exists():
                        return Response(
                            {
                                "success": False,
                                "message": f"Course {course_id} does not exist",
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except InvalidKeyError:
                    return Response(
                        {
                            "success": False,
                            "message": f"Invalid course key format: {course_id}",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Check if user exists
            try:
                user = User.objects.get(email=email)
                # User exists, check and enroll them in courses if not already enrolled
                for course_id in course_ids:
                    course_key = CourseKey.from_string(course_id)
                    # Check if already enrolled
                    if not CourseEnrollment.is_enrolled(user, course_key):
                        enrollment = CourseEnrollment.enroll(user, course_key)
                        logger.info(f"User {email} enrolled in course {course_id}")
                    else:
                        logger.info(
                            f"User {email} already enrolled in course {course_id}"
                        )
                message = (
                    f"User enrollment status verified for {len(course_ids)} course(s)"
                )
            except User.DoesNotExist:
                # User doesn't exist, create enrollment allowed if not exists
                for course_id in course_ids:
                    course_key = CourseKey.from_string(course_id)
                    # Check if enrollment allowed already exists
                    enrollment_allowed, created = (
                        CourseEnrollmentAllowed.objects.get_or_create(
                            email=email,
                            course_id=course_key,
                            defaults={"auto_enroll": True},
                        )
                    )
                    if created:
                        logger.info(
                            f"Created enrollment allowed for {email} in course {course_id}"
                        )
                    else:
                        # Update auto_enroll if needed
                        if not enrollment_allowed.auto_enroll:
                            enrollment_allowed.auto_enroll = True
                            enrollment_allowed.save()
                        logger.info(
                            f"Enrollment already allowed for {email} in course {course_id}"
                        )
                message = (
                    f"Enrollment allowance verified for {len(course_ids)} course(s)"
                )

            # Log the successful operation
            logger.info(
                f"Lernito webhook processed successfully for email: {email}, "
                f"name: {name} {family}, "
                f"course_ids: {course_ids}"
            )

            return Response({"success": True, "message": message})

        except Exception as e:
            logger.error(f"Error processing Lernito webhook: {str(e)}")
            return Response(
                {"success": False, "message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Use this payload to test the webhook
# {"email": "test@example.com", "name": "Test", "family": "User", "username": "testuser", "courseIds": ["course-v1:edX+DemoX+Demo_Course"]}
# The signature is a HMAC SHA256 hash of the request data using the webhook secret
# import hmac
# import hashlib
# import json

# # Your webhook data
# data = {
#     "email": "test@gmail.com",
#     "name": "Test",
#     "family": "User",
#     "username": "testuser",
#     "courseIds": ["course-v1:CodeTherapy+CS101011+2025_T1"]
# }

# # Convert to sorted JSON string
# data_string = json.dumps(data, sort_keys=True)

# # Generate signature
# webhook_secret = "123456"
# signature = hmac.new(
#     webhook_secret.encode('utf-8'),
#     data_string.encode('utf-8'),
#     hashlib.sha256
# ).hexdigest()

# print(f"X-Lernito-Signature: {signature}")
#
# OutPut:
# X-Lernito-Signature: 0a48a78817b613abdc3d094ca2a7ba59bddfe6d5535c99a00eefc73a6b26e64f
