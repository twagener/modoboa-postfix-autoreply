# -*- coding: utf-8 -*-

"""Postfix autoreply models."""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.utils.translation import ugettext_lazy as _

from modoboa.admin.models import Mailbox


@python_2_unicode_compatible
class ARmessage(models.Model):

    """Auto reply messages."""

    mbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    subject = models.CharField(
        _("subject"), max_length=255,
        help_text=_("The subject that will appear in sent emails")
    )
    content = models.TextField(
        _("content"),
        help_text=_("The content that will appear in sent emails")
    )
    enabled = models.BooleanField(
        _("enabled"),
        help_text=_("Activate/Deactivate your auto reply"),
        default=False
    )
    fromdate = models.DateTimeField(default=timezone.now)
    untildate = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "postfix_autoreply_armessage"

    def __str__(self):
        return smart_text("AR<{}>: {}".format(self.mbox, self.enabled))


class ARhistoric(models.Model):

    """Auto reply historic."""

    armessage = models.ForeignKey(ARmessage, on_delete=models.CASCADE)
    last_sent = models.DateTimeField(auto_now=True)
    sender = models.CharField(max_length=254)

    class Meta:
        unique_together = ("armessage", "sender")
        db_table = "postfix_autoreply_arhistoric"
