from django.db import models, transaction
from django.db.models import Sum

class TechPack(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

  def progress(self):
    return self.components.aggregate(Sum("progress"))

# Examples:
# 1:
# A random event you discover a way of removing sweat smell from ALL your stuff! Venues, band members, bar staff, the lot.
# This would look like: Tech(game_id=1, name="breath of eternally fresh air", affects="'global'", effects="{'prestige': 5}")
# 2:
# You research a dishwasher
# This would look like: Tech(game_id=1, name="dishwasher", affects="[Venue]", effects="{'prestige': 1, 'running_costs': 5}")
class Tech(models.Model):
  TECH_CATEGORIES = [(c, c) for c in [
      'event',
      'instruments',
      'location',
    ]
  ]


  PROGRESS_STAGES = [
      ('0', 'undiscovered'),
      ('1', '[|........]'),
      ('2', '[||.......]'),
      ('3', '[|||......]'),
      ('4', '[||||.....]'),
      ('5', '[|||||....]'),
      ('6', '[||||||...]'),
      ('7', '[|||||||..]'),
      ('8', '[||||||||.]'),
      ('9', 'finalizing discovery..'),
  ]

  brand = models.ManyToManyField('brand.Brand', related_name="technologies")
  pack = models.ManyToManyField("tech.TechPack", null=True, blank=True, related_name="components")
  name = models.CharField(max_length=60)
  # lasts_for = models.SmallIntegerField(default=-1) # -1 = once applied, always applied. otherwise measured in turns
  # cost_per_turn = models.SmallIntegerField(default=0) # For example hiring pyrotechnic equipment
  affects = models.CharField(max_length=255, default="'global'") # String list of models, it's a bit poo but I don't mind too much. eg [Venue, Population]
  effects = models.CharField(max_length=255, default="{'popularity': 0}") # String dict of attributes eg prestige, applied to all where attr exists. As an increment value
  category = models.CharField(max_length=27, null=True, blank=True, choices=TECH_CATEGORIES)
  progress = models.CharField(max_length=27, default=0, choices=TECH_CATEGORIES)

  def __str__(self):
    return "{} ({})".format(self.name, self.category or 'uncategorised')

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

FEATURE_SUBCATEGORIES = [(c, c) for c in [
    'wallpaper',
    'flooring',
    'bar',
    'equipment',
    'music equipment',
  ]
]

## Specific techs ##
class LocationFeature(models.Model):
  locations = models.ManyToManyField('locations.Location', null=True, blank=True, related_name="features")
  tech = models.ForeignKey('Tech', null=True, blank=True, on_delete=models.SET_NULL)
  name = models.CharField(max_length=127)
  filepath = models.CharField(max_length=127)
  width = models.PositiveSmallIntegerField()
  height = models.PositiveSmallIntegerField()
  path_d = models.CharField(max_length=2500, null=True, blank=True)
  layer = models.CharField(max_length=1, null=True, blank=True)
  category = models.CharField(max_length=27, null=True, blank=True, choices=FEATURE_SUBCATEGORIES)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['layer']
