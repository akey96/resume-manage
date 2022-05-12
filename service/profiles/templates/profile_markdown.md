# {{profile.first_name}} {{profile.last_name}}

Phone: {{profile.phone}} - Email: {{profile.email}} - github: {{profile.git}}

{{profile.description}}

## Habilidades

{% for k, v in skill_query.items %}
### {{k}}

{% for i in v %}
- {{i}}
  
{% endfor %}

{% endfor %}
