## request.POST.get() vs request.POST[]

request.POST['sth'] will raise a MultiValueDictKeyError exception if 'sth' is not in request.POST.

request.POST.get('sth') will return None if 'sth' is not in request.POST.

Additionally, .get allows you to provide an additional parameter of a default value which is returned if the key is not in the dictionary. For example, request.POST.get('sth', 'mydefaultvalue')

This is the behavior of any python dictionary and is not specific to request.POST.
