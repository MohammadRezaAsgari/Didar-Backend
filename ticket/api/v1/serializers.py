from django.db import transaction
from rest_framework import serializers

from ticket.models import Attachment, Ticket, TicketMessage
from users.api.v1.serializers import UserProfileSerializer
from users.models import Instructor


class InputTicketMessageSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(child=serializers.FileField(), required=False)

    class Meta:
        model = TicketMessage
        fields = (
            "message",
            "attachments",
        )

    @staticmethod
    def validate_attachments(value):
        """
        Check the number of attachments
        """
        if len(value) > 5:
            raise serializers.ValidationError(
                "More than 5 attachments are not allowed."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        ticket = self.context["ticket"]

        # Create the message
        attachment_data = validated_data.get("attachments", [])
        message_data = validated_data.get("message")
        message_instance = TicketMessage.objects.create(
            user=user, ticket=ticket, message=message_data
        )

        # Create attachments
        if attachment_data:
            attachments = []
            for file in attachment_data:
                if file:
                    attachments.append(
                        Attachment(
                            ticket_message=message_instance,
                            file=file,
                        )
                    )
            Attachment.objects.bulk_create(attachments)
        return message_instance


class InputTicketSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(), many=False
    )
    message = serializers.CharField(required=True)
    attachments = serializers.ListField(child=serializers.FileField(), required=False)

    class Meta:
        model = Ticket
        fields = (
            "instructor",
            "title",
            "message",
            "attachments",
        )

    @staticmethod
    def validate_attachments(value):
        if len(value) > 5:
            raise serializers.ValidationError(
                "More than 5 attachments are not allowed."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        message_data = validated_data.get("message")
        attachment_data = validated_data.get("attachments")
        instructor_obj = validated_data.get("instructor")

        # Create ticket
        ticket = Ticket.objects.create(
            user=user,
            title=validated_data.get("title"),
            instructor=instructor_obj,
        )

        # Create message
        message_instance = TicketMessage.objects.create(
            user=user, ticket=ticket, message=message_data
        )

        # Create attachments
        if attachment_data:
            attachments = []
            for file in attachment_data:
                if file:
                    attachments.append(
                        Attachment(
                            ticket_message=message_instance,
                            file=file,
                        )
                    )
            Attachment.objects.bulk_create(attachments)

        return ticket


class OutputTicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_number",
            "created",
            "title",
            "status",
        )


class InstructorOutputTicketListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_number",
            "user",
            "created",
            "title",
            "status",
        )


class OutputAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = (
            "id",
            "created",
            "file",
        )


class OutputTicketMessageSerializer(serializers.ModelSerializer):
    attachments = OutputAttachmentSerializer(many=True)
    is_mine = serializers.SerializerMethodField(source="get_is_mine")

    class Meta:
        model = TicketMessage
        fields = (
            "id",
            "created",
            "message",
            "attachments",
            "is_mine",
        )

    def get_is_mine(self, obj):
        return self.context["request"].user == obj.user


class OutputTicketDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_number",
            "created",
            "title",
            "status",
            "messages",
        )

    def get_messages(self, obj):
        messages_qs = obj.messages.all()
        return OutputTicketMessageSerializer(
            messages_qs, many=True, context=self.context
        ).data


class InstructorOutputTicketDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    user = UserProfileSerializer()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "ticket_number",
            "created",
            "user",
            "title",
            "status",
            "messages",
        )

    def get_messages(self, obj):
        messages_qs = obj.messages.all()
        return OutputTicketMessageSerializer(
            messages_qs, many=True, context=self.context
        ).data


class InstructorInputUpdateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "status",
        ]


class InstructorInputTicketMessageSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(child=serializers.FileField(), required=False)

    class Meta:
        model = TicketMessage
        fields = (
            "message",
            "attachments",
        )

    @staticmethod
    def validate_attachments(value):
        """
        Check the number of attachments
        """
        if len(value) > 5:
            raise serializers.ValidationError(
                "More than 5 attachments are not allowed."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        ticket = self.context["ticket"]

        # Change the ticket status to ANSWERED when Instructor sent a message
        ticket.status = Ticket.Status.ANSWERED
        ticket.save()

        # Create the message
        attachment_data = validated_data.get("attachments", [])
        message_data = validated_data.get("message")
        message_instance = TicketMessage.objects.create(
            user=user, ticket=ticket, message=message_data, is_student=False
        )

        # Create attachments
        if attachment_data:
            attachments = []
            for file in attachment_data:
                if file:
                    attachments.append(
                        Attachment(
                            ticket_message=message_instance,
                            file=file,
                        )
                    )
            Attachment.objects.bulk_create(attachments)

        return message_instance
