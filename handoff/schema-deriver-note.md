# Deriver note

`x-ticvai-persistence` may sit on a **property**, not only on a schema, where the schema
itself is a wrapper that is not a table. `Wishlist` is the case: the object is a projection,
the `items` array is the table.

The first version of the deriver read schema-level markers only, so `marketing.wishlist_item`
existed in the DDL and not in the reference — a table present in one artefact and absent from
the other, which is exactly the drift the reference exists to prevent.

Any future deriver must walk properties as well as schemas.
