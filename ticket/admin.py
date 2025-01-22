from django.contrib import admin
from ticket.models import Ticket, TicketMessage, Attachment


class MessageInLine(admin.TabularInline):
    model = TicketMessage
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [MessageInLine]
    list_display = [
        "ticket_number",
        "user",
        "title",
        "status",
        "created",
    ]


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin): ...


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin): ...
