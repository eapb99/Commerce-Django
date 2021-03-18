from django.forms import *

from auctions.models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['watchlist', 'lis_active','lis_user']
        widgets = {
             'category': CheckboxSelectMultiple(attrs={'type': "radio", 'style': 'color black'}) #'class': 'form-control'
         }

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, user, pk, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = 'Comment'
        self.fields['listings'].initial = Listing.objects.get(id=pk)
        self.fields['user'].initial = User.objects.get(id=user)
        self.fields['user'].widget = HiddenInput()
        self.fields['listings'].widget = HiddenInput()


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
        labels = {
            'initial': 'Bid Value'
        }
        widgets = {
            'initial': NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '$'})
        }

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        # self.fields['listings'].initial = Listing.objects.get(id=pk)
        # self.fields['user'].initial = User.objects.get(id=user)
        self.fields['user'].widget = HiddenInput()
        self.fields['listings'].widget = HiddenInput()