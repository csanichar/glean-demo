# Volta Coffee Co. — Quality Assurance & Cupping Protocol

**Document ID:** QA-001  
**Last Updated:** 2026-02-10  
**Owner:** Quality Assurance Team  
**Classification:** Internal Use Only

## Green Coffee Receiving

All incoming green coffee shipments must be inspected and approved before release to the roasting floor.

### Receiving Procedure

1. Verify lot number, origin, and weight against the purchase order in BlueCart.
2. Pull a 500g sample from three different bags in the shipment.
3. Inspect for visual defects: mold, insect damage, foreign material, excessive broken beans.
4. Measure moisture content with the Sinar 6070 meter. Acceptable range: 10.0–12.5%. Reject shipments outside this range.
5. Measure water activity with the Rotronic HygroPalm. Acceptable range: 0.50–0.60 aw.
6. Log results in the Green Coffee Intake Form (Notion database).
7. If all parameters pass, move bags to climate-controlled storage (60–70°F, 50–60% RH). If any parameter fails, quarantine the lot and notify the Sourcing Manager.

### Storage Limits

Green coffee must be used within 6 months of arrival. Lots approaching 5 months are flagged in the inventory system for priority scheduling. Lots exceeding 6 months require a re-cupping before use; if quality has degraded, the lot is donated or disposed of.

## Cupping Protocol

Volta follows the SCA Cupping Protocol with minor modifications for internal consistency.

### Sample Preparation

- Roast cupping samples on the Ikawa Pro at Volta's standard cupping profile (Profile C-1, saved in the Ikawa app under Volta QA).
- Roast to Agtron 63 ± 2 (whole bean) for consistent evaluation.
- Rest samples for 12–24 hours after roasting.

### Setup

- 12g coffee to 200ml water (1:16.67 ratio)
- Grind immediately before cupping on EK43 at setting 9.5
- Water temperature: 200°F (93.3°C), meeting SCA water quality standards
- 5 cups per sample to evaluate consistency

### Evaluation Criteria

Score each attribute on a 0–10 scale:

| Attribute | Description |
|-----------|-------------|
| Fragrance/Aroma | Dry and wet aroma intensity and quality |
| Flavor | Combined taste and retronasal aroma |
| Aftertaste | Length and quality of finish |
| Acidity | Brightness, complexity, and type (citric, malic, etc.) |
| Body | Weight and texture in the mouth |
| Balance | How well attributes complement each other |
| Uniformity | Consistency across 5 cups |
| Clean Cup | Absence of defects |
| Sweetness | Presence and quality of sweetness |
| Overall | Cupper's holistic assessment |

### Scoring Standards

- **Below 80:** Not suitable for Volta's menu. Return to sourcing for evaluation.
- **80–84:** Acceptable for batch brew and cold brew blends.
- **85–89:** Suitable for single-origin offerings and espresso blends.
- **90+:** Feature as a limited reserve offering. Notify the Marketing team for special promotion.

### Cupping Schedule

- **Production cupping:** Every roast batch is cupped within 48 hours of roasting. Minimum 2 cuppers present.
- **Green intake cupping:** Within 3 business days of receiving a new lot.
- **Blend development cupping:** Weekly on Wednesdays, 10:00 AM, at the roastery lab.
- **Calibration cupping:** Monthly with all QA staff to ensure scoring consistency.

## Roast Quality Control

### Batch Consistency

All production roasts are logged in Cropster. The roast-log-service calculates a Batch Consistency Score (BCS) for each roast based on:

- Rate of Rise (RoR) deviation from the reference profile
- Development Time Ratio (DTR) target: 20–25% of total roast time
- Drop temperature accuracy: ± 2°F of profile target

**BCS Thresholds:**
- **95–100:** Excellent. No action required.
- **85–94:** Acceptable. Review and note deviations.
- **Below 85:** Reject. Roast must be re-evaluated by the Head Roaster. If defects are confirmed, the batch is downgraded to training stock or discarded.

### Defect Tracking

Common roast defects and their causes:

- **Baked:** Insufficient heat application during development. Flat flavor, papery aftertaste.
- **Scorched:** Charge temperature too high. Dark marks on bean surface, burnt bitterness.
- **Underdeveloped:** Dropped too early. Grassy, sour, lacking sweetness.
- **Tipped:** Excessive initial heat. Dark spots on bean tips, sharp bitterness.
- **Quaker:** Not a roast defect — unripe beans that fail to color. Remove during post-roast sorting.

Log all defect occurrences in Cropster with root cause notes. If more than 2 defective batches occur in a week from the same roaster, escalate to the Head Roaster for equipment inspection and retraining.
