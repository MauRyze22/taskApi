from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Task
import resend
from decouple import config
from resend.exceptions import ResendError
import logging 

resend.api_key = config("RESEND_API_KEY")

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Task)
def obtener_asignado_de_tarea(sender, instance, **kwargs):
    if instance.pk:
        instance.asignado_a_antiguo = Task.objects.filter(pk = instance.pk).first().asignado_a
    else:
        instance.asignado_a_antiguo = None


@receiver(post_save, sender=Task)
def enviar_email_a_asignado(sender, instance, **kwargs):
    if instance.asignado_a != instance.asignado_a_antiguo and instance.asignado_a is not None:
        try:
            resend.Emails.send({
                "subject": f'Tarea asignada #{instance.pk}',
                "text": f"""
                    Hola usted ha sido asignado a la tarea #{instance.pk}
                    🎯 Contenido: {instance.contenido}
                    📝 Proyecto: {instance.proyecto.name}
                    👤 Asignado: Usted: {instance.asignado_a}
                    ⚡ Estado: {instance.estado}
                    ⚡ Fecha Limite {instance.fecha_limite}
                """,
                "from": "taskApi <onboarding@resend.dev>",
                "to": [instance.asignado_a.email],
            })
        except ResendError:
            logger.exception("No se puede enviar el email de la tarea %s", instance.pk)