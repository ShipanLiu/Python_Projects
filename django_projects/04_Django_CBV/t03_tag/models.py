from django.db import models
# django.contrib.contenttypes 在 settings.py 里面
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)
    class Meta:
        db_table = "t03_tag_tag"


class TaggedItem(models.Model):
    # a tag can be applied to many TaggedItems
    # if you delete a tag(就像下架商品一样)， it will be deleted from all items
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # 关键是： 你不知道 TaggedItems 是什么？ 可能是 (products, video, article..)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # this is the id of the target Object(products. video....)
    object_id = models.PositiveIntegerField()
    # 套路： 这个和上面的两个一起
    content_object = GenericForeignKey()

    class Meta:
        db_table = "t03_tag_taggeditem"

