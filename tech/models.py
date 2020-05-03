from django.db import models, transaction

# Examples:
# 1:
# A random event you discover a way of removing sweat smell from ALL your stuff! Venues, band members, bar staff, the lot.
# This would look like: Tech(game_id=1, name="breath of eternally fresh air", affects="'global'", effects="['prestige': 5]")
# 2:
# You research a dishwasher
# This would look like: Tech(game_id=1, name="dishwasher", affects="[Venue]", effects="{'prestige': 1, 'running_costs': -5}")
class Tech(models.Model):
  brand = models.ManyToManyField('brand.Brand', related_name="technologies")
  name = models.CharField(max_length=60)
  # lasts_for = models.SmallIntegerField(default=-1) # -1 = once applied, always applied. otherwise measured in turns
  # cost_per_turn = models.SmallIntegerField(default=0) # For example hiring pyrotechnic equipment
  affects = models.CharField(max_length=255, default="'global") # String list of models, it's a bit poo but I don't mind too much. eg [Venue, Population]
  effects = models.CharField(max_length=255, default="{'influence': 0}") # String list of attributes eg prestige, applied to all where attr exists. As an increment value

  def __str__(self):
    return self.name

  def apply(self):
    affects = eval(self.affects)
    effects = eval(self.effects)

    with transaction.atomic():
      for model in affects:
        available_attrs = [t.name for t in Tech._meta.get_fields()]
        applicable_effects = {k: v for k,v in effects.items() if k in available_attrs}
        # applicable_effects = [{k:v} for k,v in effects.items() if k in available_attrs]
        objects = model.objects.filter(brand=1)
        for o in objects:
          objects.filter(id=o.id).update(**applicable_effects)

