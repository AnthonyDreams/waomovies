import random
import string 

def rand_slug(instance):
	model_class = instance.__class__
	slugg = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
	verifing = model_class.objects.filter(slug=slugg)
	while verifing.exists():
		slugg = rand_slug()
		verifing = Article.objects.filter(slug=slugg)
		if verifing.exists():
			continue
		else:
			break
	return slugg