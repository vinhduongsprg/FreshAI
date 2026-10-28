# FreshAI — Annotation Specification v1.0

## Purpose
Train a YOLO detector to identify broad food/product categories. This version does not identify brands, exact SKUs, flavors, expiry dates, or nutritional information.

## Classes
| ID | Class | Definition |
|---:|---|---|
| 0 | canned food | Canned goods and sealed tin/container food |
| 1 | cooked chicken | Cooked chicken pieces or chicken dishes |
| 2 | dumpling | Dumplings and dumpling packages |
| 3 | egg | Individual eggs |
| 4 | fish | Fish and fish products |
| 5 | fruits | Fruit items or fruit packs grouped under a broad fruit class |
| 6 | lemon | Lemons and lemon pieces |
| 7 | meat | Meat and meat packages |
| 8 | milk | Milk containers/cartons/bottles |
| 9 | pate | Pate and similar spread/dish products |
| 10 | rice noodle | Rice noodles and noodle-based dishes |
| 11 | tomato | Tomatoes |
| 12 | vegetable | Vegetables without a separate class |
| 13 | yogurt | Yogurt cups/containers |

Examples:
- tomato → tomato
- milk carton → milk
- fish fillet/package → fish
- lemon wedge or lemon → lemon
- dumpling → dumpling
- rice noodle dish or pack → rice noodle
- fruits from the fridge shelf → fruits
- cooked chicken piece → cooked chicken

## Annotation rules
1. One physical object = one bounding box.
2. Separate identical objects get separate boxes.
3. Boxes should be reasonably tight around the visible object.
4. Clearly identifiable partially occluded objects should be labeled.
5. Do not guess ambiguous objects.
6. Label the underlying product category, not the brand.
7. Packaging is part of the product object; do not label logos, text, caps, or printed food pictures separately.
8. Food visible through transparent packaging is labeled by food category.
9. Touching objects remain separate boxes if separately identifiable.
10. Reflections and printed images are not objects.
11. Do not invent classes during annotation.
12. Out-of-scope objects remain unlabeled and should be recorded separately for possible future classes.
13. Non-food refrigerator objects are unlabeled unless later added as official classes.
14. Extremely tiny/unclear objects should not be guessed.

## Decision tree
Physical object?
- No → ignore.
- Yes → Is it in the class list?
  - No → ignore + optionally record.
  - Yes → Can it be identified confidently?
    - No → ignore.
    - Yes → draw one reasonably tight box and assign its class.

## Golden rules
- One physical object = one box.
- Identical objects get separate boxes.
- Reasonably tight boxes.
- Label clearly identifiable occluded objects.
- Never guess ambiguous objects.
- Category, not brand.
- Never invent classes mid-dataset.
- Reflections/printed images are not objects.
- Keep definitions consistent.
- When uncertain, flag instead of silently guessing.

## Pilot requirement
Before full annotation:
1. Select ~100 representative frames.
2. Annotate them using this specification.
3. Count examples per class.
4. Record ambiguous/out-of-scope objects.
5. Inspect whether any class is too broad or too rare.
6. Revise the class list if necessary.
7. Freeze v1.
8. Then annotate the full dataset.
