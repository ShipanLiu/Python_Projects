from django.conf import settings
# import signals
from django.db.models.signals import post_save
# import decorator
from django.dispatch import receiver
from store.models import Customer
"""
wie Sie ein Signal in Django verwenden können, um automatisch eine Customer-Instanz zu erstellen, sobald ein neuer Benutzer (User) erstellt wird
Die Schlüssel created und instance sind Teil der von Django bereitgestellten Argumente, die an Signal-Handler weitergegeben werden, wenn das post_save-Signal ausgelöst wird. 
Diese sind standardmäßige Schlüsselwerte und werden von Django selbst bereitgestellt. Sie müssen diese nicht explizit angeben, sondern sie werden automatisch vom Signal-System von Django übergeben.
["created"]: Dies ist ein boolescher Wert, der angibt, ob das Objekt gerade neu erstellt wurde (True) oder ob es ein bestehendes Objekt ist, das aktualisiert wurde (False).
["instance"]: Dies ist die tatsächliche Instanz des Modells, das gespeichert wurde. Im Falle eines Benutzermodells wäre es eine Instanz von User.


"""

# Das Signal wird ausgelöst, wenn ein Objekt des Modells AUTH_USER_MODEL gespeichert wird
# param "sender" is: sender ist die Modellklasse, die das Signal gesendet hat (in diesem Fall das core.user)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    """
    Überprüft, ob das Modell neu erstellt wurde. Das Signal post_save wird sowohl nach der Erstellung eines neuen Objekts als auch nach dem Aktualisieren eines bestehenden Objekts gesendet
    kwargs["created"] ist ein boolescher Wert, der angibt, ob das Objekt gerade erstellt wurde (True) oder ob es ein bestehendes Objekt ist, das aktualisiert wurde (False).
    """
    if kwargs["created"]:
        # kwargs["instance"] ist die Instanz des Benutzermodells, das gerade gespeichert wurde.
        Customer.objects.create(user=kwargs["instance"])





"""

["sender"]: Dies ist der Modellklassentyp, der das Signal ausgelöst hat. Es ist hilfreich, wenn derselbe Signal-Handler für verschiedene Modelle verwendet wird und Sie je nach Sender unterschiedliche Aktionen ausführen müssen.

["update_fields"]: Wenn das save()-Methode eines Modells aufgerufen wird, können Sie die update_fields-Option verwenden, um anzugeben, welche Felder aktualisiert werden sollen. Wenn diese Option verwendet wird, wird das update_fields-Argument im post_save Signal eine Liste dieser Felder enthalten. Dies kann nützlich sein, um zu bestimmen, ob bestimmte Aktionen basierend auf den aktualisierten Feldern durchgeführt werden sollten.

["raw"]: Dieses Argument ist ein boolescher Wert, der angibt, ob das Modell durch eine Datenbankoperation wie loaddata geladen wird. Es ist nützlich, um zu verhindern, dass der Signal-Handler während solcher Bulk-Operationen ausgelöst wird.

["using"]: Dieses Argument gibt die Datenbank an, die bei der Ausführung der save()-Methode verwendet wurde. Es kann nützlich sein, wenn Sie mit mehreren Datenbanken arbeiten und basierend darauf unterschiedliche Aktionen ausführen müssen.


"""