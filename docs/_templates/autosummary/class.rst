{{ name | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :noindex:

   {% block methods %}
   {% if all_methods %}

   .. rubric:: {{ _('Methods') }}

   .. autosummary::
      {% for item in all_methods %}
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
