from pathlib import Path

from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from utils.helpers import create_random_digits, get_hash


def attachment_path(instance, filename):
    return f"media/ticket_attachment/{get_hash(str(instance.id))}/{get_hash(filename)}{Path(filename).suffix.strip()}"


class Ticket(TimeStampedModel):
    class Status(models.IntegerChoices):
        PENDING = 1
        ANSWERED = 2
        CLOSED = 3

    ticket_number = models.CharField(
        _("ticket number"),
        max_length=10,
        unique=True,
        null=True,
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tickets",
        blank=True,
        null=True,
    )
    title = models.CharField(_("title"), max_length=255)
    instructor = models.ForeignKey(
        "users.Instructor",
        on_delete=models.SET_NULL,
        related_name="tickets",
        blank=True,
        null=True,
    )
    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.ticket_number = "#" + create_random_digits(length=8)
        super().save(*args, **kwargs)


class TicketMessage(TimeStampedModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("ticket"),
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="ticket_messages",
        blank=True,
        null=True,
        verbose_name=_("user"),
    )
    message = models.TextField(_("message"))
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ticket} - {self.user.username} - {self.message}"


class Attachment(TimeStampedModel):
    ticket_message = models.ForeignKey(
        TicketMessage,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("message"),
        blank=True,
        null=True,
    )
    file = models.FileField(
        _("file"),
        upload_to=attachment_path,
    )

    def __str__(self):
        return (
            f"{self.ticket_message.user.__str__()} {self.ticket_message.ticket.title}"
        )
