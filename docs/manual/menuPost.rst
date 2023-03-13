Post Monitors
=============

.. container:: pod

   .. rubric:: Menu menuPost
      :name: menu-menupost

   This menu is used by the long string record types to specify whether
   they should generate a monitor event only when their string value
   changes, or every time it gets written to even if the value is the
   same.

      ===== ================= =============
      Index Identifier        Choice String
      ===== ================= =============
      0     menuPost_OnChange On Change
      1     menuPost_Always   Always
      ===== ================= =============
