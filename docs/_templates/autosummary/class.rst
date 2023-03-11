{% extends "!autosummary/class.rst" %}

   {% block methods %}
   {% if all_methods %}

   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      {% for item in methods %}
      {%- if not item.startswith('_')%}
      ~{{ name }}.{{ item }}
      {%- endif -%}
      {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
      {% for item in all_attributes %}
      {%- if not item.startswith('_') %}
      ~{{ name }}.{{ item }}
      {%- endif -%}
      {%- endfor %}
   {% endif %}
   {% endblock %}
