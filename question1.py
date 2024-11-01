"""
    consider I have a model named as Brand
    mainly 4 signals in django that commonly uses
        ie, post_save, pre_save, post_delete, pre_delete
    Ans: django signals is working synchronously
        create a signals.py file
        and import that file inside the apps.py file
        in the below example pre_save will execute first and before  -
        insert a new record in the model Brand.
        and post_save will execute after a new record in model Brand and runs after insert

        def ready(self, ):
            from . import signals
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


# PRE SAVE SIGNAL FOR MODEL BRAND
@receiver(pre_save, sender=Brand)
def pre_save_req_brand(sender, **kwargs):
    print("Brand model pre save signals is triggered")


# POST SAVE SIGNAL FOR MODEL BRAND
@receiver(post_save, sender=Brand)
def post_save_req_brand(sender, instance, created, **kwargs):
    """
        CREATED HOLDS BOOLEAN VALUE
    """
    # IF A NEW OBJECT CREATED
    if created:
        print("Brand model new object created, post save")
    else:
        print("Brand model post save signals is triggered on update tasks")

# Pre-delete signal for Brand model
@receiver(pre_delete, sender=Brand)
def pre_delete_req_brand(sender, instance, **kwargs):
    print("Brand model pre delete signal is triggered")

# Post-delete signal for Brand model
@receiver(post_delete, sender=Brand)
def post_delete_req_brand(sender, instance, **kwargs):
    print("Brand model post delete signal is triggered")