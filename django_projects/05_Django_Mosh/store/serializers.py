from rest_framework import serializers


# serializer: convert "model instance" into "dictionary"
class ProductSerializer(serializers.Serializer):
    # you have to define, which attributes from tuple you want to serialize
    # don't expose your sensitive data to the outside world
    # so here you have to define exactly like defiing a model
    # 因为之后， serializer 还要接受 frontend 传来的products，这里定义max_length=255 也为了得到valid Serializer
    #the name of the attrivbutes here d't have to be the same as defined in Models
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2) # 1234.56